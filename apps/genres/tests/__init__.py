from django.test import TestCase

import copy

from genres.models import Genre

from users.tests import UserCreateMethods
from funds.tests import FundCreateMethods
from users.tests import USER_SAMPLES
from funds.tests import FUND_SAMPLES

GENRE_SAMPLES = [
    [
        {'code': '1', 'name': 'INCOME', 'is_income': True},
        {'code': '2', 'name': 'EXPENSES', 'is_income': False},
    ],
]


class GenreCreateMethods:

    def create_genre(self, user, genre, fund=None):
        genre['user'] = user
        genre['fund'] = fund

        return Genre.objects.create(**genre)


class GenresTests(TestCase, GenreCreateMethods, UserCreateMethods, FundCreateMethods):

    def setUp(self):

        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
            'genres': copy.deepcopy(GENRE_SAMPLES),
        }
