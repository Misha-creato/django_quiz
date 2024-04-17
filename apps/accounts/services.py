from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.urls import reverse
from accounts.tokens import generate_confirmation_token
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


def create_user(data):
    try:
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],
        )
        message = 'Вы успешно зарегистрировались'
    except DatabaseError as e:
        print(f'Ошибка базы данных {e}')
        message = 'Возникла ошибка, пожалуйста, попробуйте позже'
    return message


def send_confirmation_email(request, user):
    subject = 'Подтверждение адреса электронной почты'
    token = generate_confirmation_token(user=user)
    url = request.build_absolute_uri(reverse('confirm', args=(user.email, token)))
    message = f'Привет, {user.username}!\nПожалуйста, подтвердите свой адрес электронной почты, перейдя по ссылке:\n{url}'
    send_mail(subject, message, 'sanek11konek@gmail.com', [user.email])


def get_user(data):
    user = authenticate(
        username=data['username'],
        password=data['password'],
    )
    return user


def check_token(user, token):
    return default_token_generator.check_token(user=user, token=token)
