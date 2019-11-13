from django.test import TestCase

import copy

from django.contrib.auth import get_user_model

from funds.models import Fund
from genres.models import Genre

from users.tests import UserCreateMethods
from funds.tests import FundCreateMethods
from users.tests import USER_SAMPLES
from funds.tests import FUND_SAMPLES

GENRE_SAMPLES = {
    1: {'user': {'id': 1}, 'fund': {'id': 1}, 'code': '1', 'name': 'INCOME',
        'is_income': True},
    2: {'user': {'id': 1}, 'fund': {'id': 1}, 'code': '2', 'name': 'EXPENSES',
        'is_income': False},
}


class GenreCreateMethods:

    def create_genre(self, **genre):
        genre['user'] = get_user_model().objects.get(pk=genre['user']['id'])
        genre['fund'] = Fund.objects.get(pk=genre['fund']['id'])

        return Genre.objects.create(**genre)

    def create_genres(self, samples):
        for genre in samples.values():
            self.create_genre(**genre)


class GenresTests(TestCase, GenreCreateMethods, UserCreateMethods, FundCreateMethods):

    def setUp(self):

        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
            'genres': copy.deepcopy(GENRE_SAMPLES),
        }
