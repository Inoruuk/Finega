from django.contrib import admin
from django.contrib.auth.models import Group
from accounts.forms import AccountAdmin
from accounts.models import Account


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
