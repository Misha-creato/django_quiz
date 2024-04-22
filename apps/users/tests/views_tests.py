import json
import os

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.models import CustomUser
from users.views import (
    RegisterView,
    LoginView,
)


CUR_DIR = os.path.dirname(__file__)


class LoginViewTest(TestCase):
    @classmethod
    def setUp(cls):
        with open(f'{CUR_DIR}/fixtures/login.json') as file:
            cls.fixtures = json.load(file)
        cls.factory = RequestFactory()
        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_login_view_get(self):
        request = self.factory.get(reverse('login'))
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_login_view_post(self):
        for fixture in self.fixtures:
            request = self.factory.post(
                reverse('login'),
                data=fixture,
            )
            middleware = SessionMiddleware(lambda request: None)
            middleware.process_request(request)
            setattr(request, '_messages', FallbackStorage(request))
            response = LoginView.as_view()(request)
            print('code', response.status_code)
            self.assertEqual(response.status_code, fixture['status_code'])
