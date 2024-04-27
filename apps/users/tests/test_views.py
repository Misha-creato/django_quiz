import json
import os

from django.test import TestCase
from django.urls import reverse

from survey.models import (
    Survey,
    Option,
)
from users.models import CustomUser


CUR_DIR = os.path.dirname(__file__)

PATH = f'{CUR_DIR}/fixtures/views'


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('login')
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_login_view_post(self):
        fixtures = (
            (302, 'valid'),
            (400, 'invalid_1'),
            (400, 'invalid_2'),
        )

        for status in fixtures:
            with open(f'{PATH}/login_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path=self.url,
                data=data,
            )
            self.assertEqual(response.status_code, status[0])
            # 'Неправильные адрес электронной почты или пароль'


class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('register')

    def test_register_view_post(self):
        fixtures = (
            (302, 'valid'),
            (400, 'invalid_1'),
            (400, 'invalid_2'),
        )

        for status in fixtures:
            with open(f'{PATH}/register_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path=self.url,
                data=data,
            )

            self.assertEqual(response.status_code, status[0])


class EmailConfirmViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
            url_hash="e932ebd3-4e5a-4dd5-ade3-62c815ff3e0a",
        )

    def test_email_confirm_view_get(self):
        fixtures = (
            'valid',
            'invalid',
        )

        for status in fixtures:
            with open(f'{PATH}/email_confirm_view_{status}_request.json') as file:
                url_hash = json.load(file)

            with open(f'{PATH}/email_confirm_view_{status}_response.json') as file:
                response_message = json.load(file)

            url = reverse('confirm_email', args=(url_hash,))

            response = self.client.get(
                path=url,
                follow=True,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)


class SettingsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('settings')
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_settings_view_post(self):
        fixtures = (
            'valid',
            'invalid',
        )

        for status in fixtures:
            with open(f'{PATH}/settings_view_{status}_request.json') as file:
                data = json.load(file)

            with open(f'{PATH}/settings_view_{status}_response.json') as file:
                response_message = json.load(file)

            self.client.login(
                email='test1@example.com',
                password='password123'
            )
            response = self.client.post(
                path=self.url,
                data=data,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)


class StatsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('stats')
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_stats_view_get(self):
        survey = Survey.objects.create(
            question='How are you?',
        )
        option = Option.objects.create(
            survey=survey,
            title='Answer',
        )
        self.user.options.add(option.id)

        self.client.login(
            email='test1@example.com',
            password='password123'
        )
        response = self.client.get(
            path=self.url,
        )
        expected_result = (Survey.objects.filter(options__users=self.user.id)
                           .prefetch_related('options'))

        context_data = response.context

        self.assertEqual(response.status_code, 200)
        self.assertIn('surveys', context_data)
        self.assertQuerysetEqual(context_data['surveys'], expected_result)


class PasswordResetRequestViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('password_reset_request')
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_password_reset_request_view_post(self):
        fixtures = (
                'valid',
                'invalid',
            )

        for status in fixtures:
            with open(f'{PATH}/password_reset_request_view_{status}_request.json') as file:
                data = json.load(file)

            with open(f'{PATH}/password_reset_request_view_{status}_response.json') as file:
                response_message = json.load(file)

            response = self.client.post(
                path=self.url,
                data=data,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)


class PasswordResetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
            url_hash="e932ebd3-4e5a-4dd5-ade3-62c815ff3e0a",
        )

    def test_password_reset_view_get(self):
        fixtures = (
                200,
                302,
            )

        for status in fixtures:
            with open(f'{PATH}/password_reset_view_{status}_request.json') as file:
                url_hash = json.load(file)

            url = reverse('password_reset', args=(url_hash,))

            response = self.client.get(
                path=url,
            )

            self.assertEqual(response.status_code, status)

    def test_password_reset_view_post(self):
        fixtures = (
                'valid',
                'invalid',
            )

        for status in fixtures:
            with open(f'{PATH}/password_reset_view_{status}_request.json') as file:
                data = json.load(file)

            with open(f'{PATH}/password_reset_view_{status}_response.json') as file:
                response_message = json.load(file)

            url = reverse('password_reset', args=(self.user.url_hash,))

            response = self.client.post(
                path=url,
                data=data,
                follow=True,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)
