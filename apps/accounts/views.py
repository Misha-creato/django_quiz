from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import (
    login,
    get_user_model,
)


from accounts.forms import CustomUserCreationForm
from accounts.services import (
    create_user,
    get_user,
    send_confirmation_email,
    check_token,
)

User = get_user_model()


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='register.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = CustomUserCreationForm(data)
        if form.is_valid():
            message = create_user(data=data)
            messages.success(request=request, message=message)
            return redirect('login')
        context = {
            'error_messages': form.errors.items()
        }
        return render(request=request, template_name='register.html', context=context)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='login.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = get_user(data=data)
        if user is not None:
            login(request=request, user=user)
            # send_confirmation_email(request=request, user=user)
            return redirect('index')
        messages.error(request=request, message='Неправильное имя пользователя или пароль')
        return render(request=request, template_name='login.html')


class EmailConfirmView(View):
    def get(self, request, email, token):
        user = User.objects.get(email=email)
        if check_token(user=user, token=token):
            user.email_confirmed = True
            user.save()
            return redirect('index')


def profile_view(request):
    return render(request=request, template_name='profile.html')


def settings_view(request):
    return render(request=request, template_name='settings.html')


def stats_view(request):
    return render(request=request, template_name='stats.html')