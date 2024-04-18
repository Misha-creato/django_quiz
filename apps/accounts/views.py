from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    login,
    logout,
)

from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from accounts.models import CustomUser as User
from accounts.forms import CustomUserCreationForm
from accounts.services import (
    create_user,
    get_user,
    set_form_error_messages,
)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='register.html'
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = CustomUserCreationForm(data)
        if form.is_valid():
            create_user(
                request=request,
                data=data
            )
            return redirect('login')
        set_form_error_messages(
            request=request,
            form=form
        )
        return render(
            request=request,
            template_name='register.html'
        )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='login.html'
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = get_user(data=data)
        if user is not None:
            login(
                request=request,
                user=user
            )
            return redirect('index')
        messages.error(
            request=request,
            message='Неправильные адрес электронной почты или пароль'
        )
        return render(
            request=request,
            template_name='login.html'
        )


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request=request)
        return redirect('index')


class EmailConfirmView(View):
    def get(self, request, token):
        user = User.objects.get(token=token)
        if user:
            user.email_confirmed = True
            user.save()
            messages.success(
                request=request,
                message='Адрес электронной почты успешно подтвержден'
            )
            return redirect('index')
        messages.error(
            request=request,
            message='Неверный токен'
        )


class SettingsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='settings.html'
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request=request,
                message='Пароль успешно изменен'
            )
            update_session_auth_hash(
                request=request,
                user=user
            )
            return render(
                request=request,
                template_name='settings.html'
            )
        set_form_error_messages(
            request=request,
            form=form
        )
        return render(
            request=request,
            template_name='settings.html'
        )


def stats_view(request):
    return render(
        request=request,
        template_name='stats.html'
    )
