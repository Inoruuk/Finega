from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)


def user_directory_path(instance, filename):
    # upload to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Department(models.Model):
    name = models.CharField(
        max_length=255
    )
    icon = models.FileField(
        upload_to='uploads/'
    )
    child = models.ForeignKey(
        "self",
        on_delete=models.CASCADE
    )


class Role(models.Model):
    name = models.CharField(
        max_length=255
    )
    icon = models.FileField(
        upload_to='uploads/'
    )


class Job(models.Model):
    name = models.CharField(
        max_length=255
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT
    )


class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, first_name, last_name, phone):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a surname')
        if not last_name:
            raise ValueError('Users must have a lastname')
        user = self.model(
            email=self.normalize_email(email),
            username=(first_name[0] + last_name).lower(),
            first_name=first_name.lower(),
            last_name=last_name.lower(),
            phone=phone
        )
        password = self.make_random_password(
            length=10,
            allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'
        )
        print(password)
        user.set_password(password)
        user.save(using=self._db)
        user.email_account(
            subject="[OSIA] Do Not Reply - Account Activation",
            message=render_to_string('accounts/activation_email.html',
                                     {
                                         'user': user,
                                         'password': password
                                     }
                                     )
        )
        return user

    def create_superuser(self, email, first_name, last_name, phone):
        """
        Creates and saves a superuser with the given email, first name,
        last name and phone.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Class dedicated to custom user model: AUTH_USER_MODEL.
    """
    email = models.EmailField(
        _('email'),
        max_length=255,
        unique=True
    )
    username = models.CharField(
        _('username'),
        max_length=255
    )
    first_name = models.CharField(
        _('first name'),
        max_length=255
    )
    last_name = models.CharField(
        _('last name'),
        max_length=255
    )
    phone = models.CharField(
        _('phone number'),
        max_length=12
    )
    job = models.ManyToManyField(
        Job
    )
    date_joined = models.DateField(
        _('date joined'),
        default=timezone.now
    )
    avatar = models.ImageField(
        _('avatar'),
        upload_to='uploads/'
    )
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    is_admin = models.BooleanField(
        _('admin'),
        default=False
    )

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def set_email(self, email):
        if email and self.email and self.email != email:
            self.email = email
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_account(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_admin
