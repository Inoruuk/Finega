from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.template.defaultfilters import capfirst
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (authenticate, password_validation)
from accounts.models import Account


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.CharField(
        label=_("Email"),
        widget=forms.EmailInput,
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _("Wrong %(email)s or password."),
        'inactive': _("Sorry, this account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "email" field.
        self.username_field = Account._meta.get_field(Account.USERNAME_FIELD)
        self.fields['email'].max_length = self.username_field.max_length or 254
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                try:
                    user_tmp = Account.objects.get(email=email)
                except Account.DoesNotExist:
                    user_tmp = None
                if user_tmp is not None and user_tmp.check_password(raw_password=password):
                    self.confirm_login_allowed(user_tmp)
                else:
                    raise self.get_invalid_login_error()
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.username_field.verbose_name},
        )


class AccountResetPasswordForm(forms.Form):
    """A form for sending reset password instructions with
    given email."""
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput
    )
    error_messages = {
        'invalid_login': _("Wrong email."),
        'inactive': _("Sorry, this account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.username_field = Account._meta.get_field(Account.USERNAME_FIELD)
        self.fields['email'].max_length = self.username_field.max_length or 254
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        if email is not None:
            try:
                user_tmp = Account.objects.get(email=email)
            except Account.DoesNotExist:
                user_tmp = None
            if user_tmp is not None:
                if not user_tmp.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
                else:
                    user_tmp.email_account(
                        subject="[OSIA] Do Not Reply - Reset Password Instructions",
                        message=render_to_string('accounts/activation_email.html',
                                                 {
                                                     'user': user_tmp.username,
                                                     'password': user_tmp.password
                                                 }
                                                 )
                    )
            else:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
        return email


class AccountCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # surname = forms.CharField(label='Surname', widget=forms.TextInput)
    # lastname = forms.CharField(label='Lastname', widget=forms.TextInput)
    # phone = forms.CharField(label='Phone', widget=forms.TextInput)
    # avatar = forms.ImageField(label='Avatar')
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput
    )
    email2 = forms.CharField(
        label='Email Confirmation',
        widget=forms.EmailInput,
        help_text='Required. Inform a valid email address.'
    )

    class Meta:
        model = Account
        fields = ('avatar', 'email', 'email2', 'first_name', 'last_name', 'phone')

    def match_email(self):
        # Check that the two password entries match
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if not email and email2 and email != email2:
            raise forms.ValidationError("Emails don't match")
        return email2

    def save(self, commit=True):
        # Save the provided password in hashed format
        account = super().save(commit=False)
        if self.match_email():
            account.save(commit)
        return account


class AccountChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'first_name', 'last_name', 'phone')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AccountAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone', 'date_joined', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'email2', 'first_name', 'last_name', 'phone')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
