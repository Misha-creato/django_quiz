import uuid

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
)

from django.core.mail import send_mail
from django.urls import reverse

from config.settings import EMAIL_HOST_USER
from users.models import CustomUser


def create_and_return_user(request, data):
    try:
        user = CustomUser.objects.create_user(
            email=data['email'],
            password=data['password1'],
        )
        messages.success(
            request=request,
            message='Вы успешно зарегистрировались'
        )
        return user
    except Exception as exc:
        print(f'Не удалось создать пользователя {exc}')
        messages.error(
            request=request,
            message='Возникла ошибка при создании пользователя, пожалуйста, попробуйте позже'
        )
        return None


def send_mail_to_user(request, user, password_reset=False):
    url_hash = get_user_url_hash(user=user)
    url = request.build_absolute_uri(reverse('confirm', args=(url_hash,)))

    subject = 'Подтверждение адреса электронной почты'
    message = (
        f'Добро пожаловать на наш сайт!\n'
        f'Пожалуйста, подтвердите свой адрес электронной почты, перейдя по ссылке:\n{url}'
    )
    if password_reset:
        url = request.build_absolute_uri(reverse('password_reset', args=(url_hash,)))
        subject = 'Восстановление пароля'
        message = (
            f'Восстановления пароля на сайте\n'
            f'Чтобы сбросить пароль на сайте, перейдите по ссылке:\n{url}'
        )
    send_mail(subject, message, EMAIL_HOST_USER, [user.email])


def is_user_logged_in(request, data):
    user = authenticate(
        request=request,
        username=data['email'],
        password=data['password'],
    )
    if user is not None:
        login(
            request=request,
            user=user,
        )
        return True
    return False


def set_form_error_messages(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(
                request=request,
                message=error
            )


def get_user_url_hash(user):
    url_hash = str(uuid.uuid4())
    user.url_hash = url_hash
    user.save()
    return url_hash
