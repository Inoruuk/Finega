# https://docs.djangoproject.com/en/2.2/ref/class-based-views/
from django.shortcuts import (render, redirect)
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth import (login, logout, authenticate)
from django.contrib.auth import decorators
from django.utils.decorators import method_decorator
from accounts.forms import (AccountCreationForm, AccountChangeForm, AuthenticationForm, AccountResetPasswordForm)
from django.conf import settings

users = [
    'production',
    'engineering',
    'maintenance'
]

emails = {
    'production': 'production@finega.com',
    'engineering': 'engineeing@finega.com',
    'maintenance': 'maintenance@finega.com'
}

passwords = {
    'production': 'wKD5L4bQqG',
    'engineering': 'vxJK3xTpMY',
    'maintenance': '4P8rfuHnU9'
}


@method_decorator([decorators.user_passes_test(lambda u: not u.is_authenticated, login_url=settings.LOGIN_REDIRECT_URL)], name='dispatch')
class AuthenticationDemoView(View):

    def get(self, request):
        template = ''
        for user in users:
            if request.GET.get('next') == user:
                login(request, authenticate(request, username=emails[user], password=passwords[user]))
                return redirect('dashboard_home')
        return render(request, 'accounts/authenticationDemo.html')


@method_decorator([decorators.user_passes_test(lambda u: not u.is_authenticated, login_url=settings.LOGIN_REDIRECT_URL)], name='dispatch')
class AuthenticationLoginView(FormView):
    template_name = 'accounts/authenticationLogin.html'
    form_class = AuthenticationForm
    success_url = settings.LOGOUT_REDIRECT_URL

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        email = form.cleaned_data['email']
        login(self.request, form.user_cache)
        return super().form_valid(form)


@method_decorator([decorators.user_passes_test(lambda u: not u.is_authenticated, login_url=settings.LOGIN_REDIRECT_URL)], name='dispatch')
class AuthenticationResetView(FormView):
    template_name = 'accounts/authenticationReset.html'
    form_class = AccountResetPasswordForm
    success_url = settings.LOGIN_URL

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)
