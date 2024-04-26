import json
import os
import random

from django.test import TestCase

from survey.models import (
    Survey,
    Option,
)
from users.models import CustomUser


CUR_DIR = os.path.dirname(__file__)


class SurveyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        with open(f'{CUR_DIR}/fixtures/users.json') as file:
            cls.users_fixtures = json.load(file)

        with open(f'{CUR_DIR}/fixtures/option.json') as file:
            cls.option_fixtures = json.load(file)

        cls.survey = Survey.objects.create(
            question="Question",
            description="Description",
        )

    def test_count_voted(self):
        users = []
        options = []
        for fixture in self.option_fixtures:
            option = Option.objects.create(
                survey=self.survey,
                **fixture,
            )
            options.append(option)

        for fixture in self.users_fixtures:
            user = CustomUser.objects.create(
                email=fixture['email'],
                password=fixture['password']
            )
            user.options.add(random.choice(options).id)
            users.append(user)

        self.assertEqual(self.survey.count_voted, len(users))
