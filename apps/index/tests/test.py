from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from survey.models import (
    Option,
    Survey,
)


User = get_user_model()


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('index')
        cls.user = User.objects.create_user(
            email="test1@example.com",
            password="password123",
        )

    def test_index_view_post(self):
        survey = Survey.objects.create(
            question='How are you?',
        )
        option = Option.objects.create(
            survey=survey,
            title='Answer',
        )
        data = {
            'option': option.id,
        }

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
        self.assertEqual(str(messages[0]), 'Спасибо, Ваш выбор учтён. Вы можете просмотреть статистику в профиле.')
        self.assertEqual(response.status_code, 302)
