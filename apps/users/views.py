from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import F
from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from users.models import CustomUser
from users.forms import CustomUserCreationForm
from users.services import (
    create_user,
    is_user_logged_in,
    set_form_error_messages,
)

from survey.models import Survey


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='register.html',
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = CustomUserCreationForm(data)
        if form.is_valid():
            create_user(
                request=request,
                data=data,
            )
            return redirect('login')
        set_form_error_messages(
            request=request,
            form=form,
        )
        return render(
            request=request,
            template_name='register.html',
        )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='login.html',
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        if is_user_logged_in(request=request, data=data):
            return redirect('index')
        messages.error(
            request=request,
            message='Неправильные адрес электронной почты или пароль',
        )
        return render(
            request=request,
            template_name='login.html',
        )


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request=request)
        return redirect('index')


class EmailConfirmView(View):
    def get(self, request, url_hash):
        user = CustomUser.objects.filter(url_hash=url_hash)
        if user.exists():
            user = user.first()
            user.email_confirmed = True
            user.url_hash = ''
            user.save()
            messages.success(
                request=request,
                message='Адрес электронной почты успешно подтвержден',
            )
        else:
            messages.error(
                request=request,
                message='Неверный токен',
            )
        return redirect('index')


class SettingsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='settings.html',
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request=request,
                message='Пароль успешно изменен',
            )
            update_session_auth_hash(
                request=request,
                user=user,
            )
        else:
            set_form_error_messages(
                request=request,
                form=form,
            )
        return render(
            request=request,
            template_name='settings.html',
        )


class StatsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user.id
        surveys = (Survey.objects.filter(options__users=user)
                   .annotate(user_answer=F('options__title'))
                   .prefetch_related('options'))
        context = {
            'surveys': surveys
        }
        return render(
            request=request,
            template_name='stats.html',
            context=context,
        )
