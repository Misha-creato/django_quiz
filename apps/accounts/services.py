from django.contrib.auth import authenticate
from django.contrib import messages

from django.core.mail import send_mail
from django.urls import reverse

from accounts.tokens import generate_confirmation_token
from accounts.models import CustomUser as User


def create_user(request, data):
    try:
        user = User.objects.create_user(
            email=data['email'],
            password=data['password1'],
        )
        messages.success(
            request=request,
            message='Вы успешно зарегистрировались'
        )
        send_confirmation_email(request=request, user=user)
    except Exception as exc:
        print(f'Не удалось создать пользователя {exc}')
        messages.error(
            request=request,
            message='Возникла ошибка при создании пользователя, пожалуйста, попробуйте позже'
        )


def send_confirmation_email(request, user):
    subject = 'Подтверждение адреса электронной почты'
    token = get_user_token(user=user)
    url = request.build_absolute_uri(reverse('confirm', args=(token,)))
    message = (
        f'Привет, {user.username}!\n'
        f'Пожалуйста, подтвердите свой адрес электронной почты, перейдя по ссылке:\n{url}'
    )
    send_mail(subject, message, 'example@gmail.com', [user.email])


def get_user(data):
    user = authenticate(
        username=data['email'],
        password=data['password'],
    )
    return user


def set_form_error_messages(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(
                request=request,
                message=error
            )


def get_user_token(user):
    token = generate_confirmation_token(user=user)
    user.token = token
    user.save()
    return token
