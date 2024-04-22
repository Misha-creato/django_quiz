from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
)

from django.db.models import F
from django.views import View
from django.shortcuts import (
    render,
    redirect,
)

from users.models import CustomUser
from users.forms import CustomUserCreationForm
from users.services import (
    create_and_return_user,
    is_user_logged_in,
    set_form_error_messages,
    send_mail_to_user,
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
            user = create_and_return_user(
                request=request,
                data=data,
            )
            if user is not None:
                send_mail_to_user(request=request, user=user)
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


class PasswordResetRequestView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name='password_reset.html',
        )

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            user = user.first()
            send_mail_to_user(
                request=request,
                user=user,
                password_reset=True,
            )
            messages.success(
                request=request,
                message='Письмо для сброса пароля отправлено. Проверьте свой почтовый ящик.',
            )
            form_sent = True
        else:
            messages.error(
                request=request,
                message='Пользователь с таким адресом электронной почты не найден.',
            )
            form_sent = False
        context = {
            'form_sent': form_sent,
        }
        return render(
            request=request,
            template_name='password_reset.html',
            context=context,
        )


class PasswordResetView(View):
    def get(self, request, url_hash):
        user = CustomUser.objects.filter(url_hash=url_hash)
        if user.exists():
            return render(
                request=request,
                template_name='password_reset_form.html',
            )
        messages.error(
            request=request,
            message='Неверный токен',
        )
        return redirect('login')

    def post(self, request, url_hash, **kwargs):
        user = CustomUser.objects.filter(url_hash=url_hash).first()
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user.url_hash = ''
            user.save()
            form.save()
            messages.success(
                request=request,
                message='Пароль успешно изменен',
            )
            return redirect('login')
        else:
            set_form_error_messages(
                request=request,
                form=form,
            )
        return render(
            request=request,
            template_name='password_reset_form.html',
        )
