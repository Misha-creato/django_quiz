import json
import os
import uuid

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
)

from django.core.mail import send_mail
from django.urls import reverse

from config.settings import (
    EMAIL_HOST_USER,
    SEND_EMAILS,
)

from users.models import CustomUser


CUR_DIR = os.path.dirname(__file__)


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


def send_mail_to_user(request, user, action):
    url_hash = get_user_url_hash(user=user)
    url = request.build_absolute_uri(reverse(action, args=(url_hash,)))

    with open(f'{CUR_DIR}/mail_messages/{action}.json') as file:
        data = json.load(file)

    subject = data['subject']
    message = data['message'].format(url=url)

    if SEND_EMAILS:
        send_mail(subject, message, EMAIL_HOST_USER, [user.email])
    else:
        print('Отправка писем отключена')


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
