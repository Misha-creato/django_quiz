import json
import os

from django.test import TestCase

from users.models import CustomUser
from users.services import is_user_logged_in


CUR_DIR = os.path.dirname(__file__)


class ServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = f'{CUR_DIR}/fixtures/services'

        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_is_user_logged_in(self):
        response = self.client.get('/')
        request = response.wsgi_request

        fixtures = (
            True,
            False,
        )

        for status in fixtures:
            with open(f'{self.path}/is_user_logged_in_{status}_request.json') as file:
                data = json.load(file)

            user_logged = is_user_logged_in(request, data)

            self.assertEqual(user_logged, status, msg=status)
