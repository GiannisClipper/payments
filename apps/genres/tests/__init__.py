from django.test import TestCase

import copy

from django.contrib.auth import get_user_model

from funds.models import Fund
from genres.models import Genre

from users.tests import UserCreateMethods
from funds.tests import FundCreateMethods

from users.tests import USER_SAMPLES, ADMIN_SAMPLES
from funds.tests import FUND_SAMPLES

GENRE_SAMPLES = {
    # First key digit is equal to user id

    11: {'user': {'id': 1}, 'fund': {'key': 11}, 'code': '1', 'name': 'INCOMING',
        'is_incoming': True},  # noqa: E127
    12: {'user': {'id': 1}, 'fund': {'key': 11}, 'code': '2', 'name': 'OUTGOING',
        'is_incoming': False},  # noqa: E127
    21: {'user': {'id': 2}, 'fund': {'key': 21}, 'code': 'ES', 'name': 'ESODA',
        'is_incoming': True},  # noqa: E127
    22: {'user': {'id': 2}, 'fund': {'key': 21}, 'code': 'EX', 'name': 'EXODA',
        'is_incoming': False},  # noqa: E127
}


class GenreCreateMethods:

    def create_genre(self, **genre):
        genre['user'] = get_user_model().objects.get(pk=genre['user']['id'])
        genre['fund'] = Fund.objects.get(pk=genre['fund']['id'])

        return Genre.objects.create(**genre)

    def create_genres(self, samples):
        for sample in samples.values():
            genre = self.create_genre(**sample)
            sample['id'] = genre.pk


class GenresTests(TestCase, GenreCreateMethods, UserCreateMethods, FundCreateMethods):

    def setUp(self):

        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'admins': copy.deepcopy(ADMIN_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
            'genres': copy.deepcopy(GENRE_SAMPLES),
        }

        self.create_users(self.samples['users'])
        self.create_admins(self.samples['admins'])
        self.create_funds(self.samples['funds'])

        for sample in self.samples['genres'].values():
            key = sample['fund']['key']
            sample['fund']['id'] = self.samples['funds'][key]['id']
            sample['fund'].pop('key', None)
