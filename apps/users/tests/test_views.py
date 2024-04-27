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


class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = f'{CUR_DIR}/fixtures/views'
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
            url_hash="e932ebd3-4e5a-4dd5-ade3-62c815ff3e0a",
        )

    def test_login_view_post(self):
        url = reverse('login')
        fixtures = (
            (200, 'valid'),
            (401, 'invalid_1'),
            (401, 'invalid_2'),
            (400, 'invalid'),
        )

        for status in fixtures:
            with open(f'{self.path}/login_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path=url,
                data=data,
                follow=True,
            )

            self.assertEqual(response.status_code, status[0], msg=status)

    def test_register_view_post(self):
        url = reverse('register')

        fixtures = (
            (200, 'valid'),
            (400, 'invalid_1'),
            (400, 'invalid_2'),
            (400, 'invalid_3'),
        )

        for status in fixtures:
            with open(f'{self.path}/register_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path=url,
                data=data,
                follow=True,
            )

            self.assertEqual(response.status_code, status[0], msg=status)

    def test_email_confirm_view_get(self):
        fixtures = (
            'valid',
            'invalid',
        )

        for status in fixtures:
            with open(f'{self.path}/email_confirm_view_{status}_request.json') as file:
                url_hash = json.load(file)

            with open(f'{self.path}/email_confirm_view_{status}_response.json') as file:
                response_message = json.load(file)

            url = reverse('confirm_email', args=(url_hash,))

            response = self.client.get(
                path=url,
                follow=True,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)

    def test_settings_view_post(self):
        url = reverse('settings')
        fixtures = (
            (200, 'valid'),
            (400, 'invalid_1'),
            (400, 'invalid_2'),
        )

        for status in fixtures:
            with open(f'{self.path}/settings_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            with open(f'{self.path}/settings_view_{status[0]}_{status[1]}_response.json') as file:
                response_message = json.load(file)

            self.client.login(
                email='test1@example.com',
                password='password123'
            )
            response = self.client.post(
                path=url,
                data=data,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(response.status_code, status[0], msg=status)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)

    def test_stats_view_get(self):
        url = reverse('stats')
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
            path=url,
        )
        expected_result = (Survey.objects.filter(options__users=self.user.id)
                           .prefetch_related('options'))

        context_data = response.context

        self.assertEqual(response.status_code, 200)
        self.assertIn('surveys', context_data)
        self.assertQuerysetEqual(context_data['surveys'], expected_result)

    def test_password_reset_request_view_post(self):
        url = reverse('password_reset_request')
        fixtures = (
            (200, 'valid'),
            (400, 'invalid_1'),
            (400, 'invalid_2'),
        )

        for status in fixtures:
            with open(f'{self.path}/password_reset_request_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            with open(f'{self.path}/password_reset_request_view_{status[0]}_{status[1]}_response.json') as file:
                response_message = json.load(file)

            response = self.client.post(
                path=url,
                data=data,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(response.status_code, status[0], msg=status)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)

    def test_password_reset_view_get(self):
        fixtures = (
            200,
            302,
        )

        for status in fixtures:
            with open(f'{self.path}/password_reset_view_{status}_request.json') as file:
                url_hash = json.load(file)

            url = reverse('password_reset', args=(url_hash,))

            response = self.client.get(
                path=url,
            )

            self.assertEqual(response.status_code, status, msg=status)

    def test_password_reset_view_post(self):
        fixtures = (
            (200, 'valid'),
            (400, 'invalid_1'),
            (400, 'invalid_2'),
        )

        for status in fixtures:
            with open(f'{self.path}/password_reset_view_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            with open(f'{self.path}/password_reset_view_{status[0]}_{status[1]}_response.json') as file:
                response_message = json.load(file)

            url = reverse('password_reset', args=(self.user.url_hash,))

            response = self.client.post(
                path=url,
                data=data,
                follow=True,
            )

            messages = list(response.wsgi_request._messages)
            self.assertEqual(response.status_code, status[0], msg=status)
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), response_message)
