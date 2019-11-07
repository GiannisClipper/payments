from django.test import TestCase

import copy

from genres.models import Genre

from users.tests import SAMPLES as USERS_SAMPLES
from funds.tests import SAMPLES as FUNDS_SAMPLES

SAMPLES = [
    [
        {'code': '1', 'name': 'INCOME', 'is_income': True},
        {'code': '2', 'name': 'EXPENSES', 'is_income': False},
    ],
]


class GenresTests(TestCase):

    def setUp(self):

        self.samples = {
            'users': copy.deepcopy(USERS_SAMPLES),
            'funds': copy.deepcopy(FUNDS_SAMPLES),
            'genres': copy.deepcopy(SAMPLES),
        }

    @staticmethod
    def create_genre(user, genre, fund=None):

        genre['user'] = user
        genre['fund'] = fund

        return Genre.objects.create(**genre)
