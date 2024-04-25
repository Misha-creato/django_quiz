import json
import os

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from unittest.mock import patch
from config.settings import EMAIL_HOST_USER

from users.models import CustomUser
from users.services import (
    create_and_return_user,
    is_user_logged_in,
    send_mail_to_user,
)


CUR_DIR = os.path.dirname(__file__)


class ServiceTests(TestCase):
    @classmethod
    def setUp(cls):
        with open(f'{CUR_DIR}/fixtures/create_user.json') as file:
            cls.create_user_fixtures = json.load(file)

        with open(f'{CUR_DIR}/fixtures/login_user.json') as file:
            cls.login_user_fixtures = json.load(file)

        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )
        cls.factory = RequestFactory()
        cls.request = cls.factory.get('/')
        cls.request.session = {}
        middleware = SessionMiddleware(lambda request: None)
        middleware.process_request(cls.request)
        cls.messages = FallbackStorage(cls.request)
        cls.request._messages = cls.messages

    def test_create_user(self):
        for fixture in self.create_user_fixtures:
            user = create_and_return_user(
                request=self.request,
                data=fixture,
            )
            if fixture['expected_result'] is None:
                self.assertIsNone(user)
            else:
                self.assertIsNotNone(user)
                self.assertEqual(user.email, fixture['email'])

    def test_is_user_logged_in(self):
        for fixture in self.login_user_fixtures:
            response = is_user_logged_in(
                request=self.request,
                data=fixture,
            )
            self.assertEqual(response, fixture['expected_result'])

    @patch('users.services.send_mail')
    def test_send_mail_to_user_confirm(self, mock_send_mail):
        send_mail_to_user(self.request, self.user)
        url = self.request.build_absolute_uri(reverse('confirm', args=(self.user.url_hash,)))

        mock_send_mail.assert_called_once_with(
            'Подтверждение адреса электронной почты',
            f'Добро пожаловать на наш сайт!\n'
            f'Пожалуйста, подтвердите свой адрес электронной почты, перейдя по ссылке:\n'
            f'{url}',
            EMAIL_HOST_USER,
            [self.user.email]
        )

    @patch('users.services.send_mail')
    def test_send_mail_to_user_reset_password(self, mock_send_mail):
        send_mail_to_user(self.request, self.user, password_reset=True)
        url = self.request.build_absolute_uri(reverse('password_reset', args=(self.user.url_hash,)))

        mock_send_mail.assert_called_once_with(
            'Восстановление пароля',
            f'Восстановления пароля на сайте\n'
            f'Чтобы сбросить пароль на сайте, перейдите по ссылке:\n'
            f'{url}',
            EMAIL_HOST_USER,
            [self.user.email]
        )


