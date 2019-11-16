from django.test import TestCase

import copy

from django.contrib.auth import get_user_model

from funds.models import Fund
from genres.models import Genre
from payments.models import Payment

from users.tests import UserCreateMethods
from funds.tests import FundCreateMethods
from genres.tests import GenreCreateMethods

from users.tests import USER_SAMPLES, ADMIN_SAMPLES
from funds.tests import FUND_SAMPLES
from genres.tests import GENRE_SAMPLES

PAYMENT_SAMPLES = {
    # First key digit is equal to user id

    11: {'user': {'id': 1}, 'date': '2019-10-30', 'incoming': 22.5, 'outgoing': None,
        'fund': {'key': 11}, 'genre': {'key': 11}, 'remarks': 'Incoming...'},  # noqa: E127
    12: {'user': {'id': 1}, 'date': '2019-10-31', 'incoming': 18.5, 'outgoing': None,
        'fund': {'key': 12}, 'genre': {'key': 11}, 'remarks': 'Incoming...'},  # noqa: E127
    13: {'user': {'id': 1}, 'date': '2019-11-02', 'incoming': None, 'outgoing': 10.0,
        'fund': {'key': 11}, 'genre': {'key': 12}, 'remarks': 'outgoing...'},  # noqa: E127
    14: {'user': {'id': 1}, 'date': '2019-11-03', 'incoming': None, 'outgoing': 11.0,
        'fund': {'key': 12}, 'genre': {'key': 12}, 'remarks': 'outgoing...'},  # noqa: E127

    21: {'user': {'id': 2}, 'date': '2019-11-01', 'incoming': 15.0, 'outgoing': None,
        'fund': {'key': 21}, 'genre': {'key': 21}, 'remarks': 'Incoming...'},  # noqa: E127
    22: {'user': {'id': 2}, 'date': '2019-11-02', 'incoming': None, 'outgoing': 20.0,
        'fund': {'key': 21}, 'genre': {'key': 22}, 'remarks': 'outgoing...'},  # noqa: E127
}


class PaymentCreateMethods:

    def create_payment(self, **payment):
        payment['user'] = get_user_model().objects.get(pk=payment['user']['id'])
        payment['fund'] = Fund.objects.get(pk=payment['fund']['id'])
        payment['genre'] = Genre.objects.get(pk=payment['genre']['id'])

        return Payment.objects.create(**payment)

    def create_payments(self, samples):
        for sample in samples.values():
            payment = self.create_payment(**sample)
            sample['id'] = payment.pk


class PaymentsTests(TestCase, PaymentCreateMethods, GenreCreateMethods,
                    UserCreateMethods, FundCreateMethods):

    def setUp(self):

        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'admins': copy.deepcopy(ADMIN_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
            'genres': copy.deepcopy(GENRE_SAMPLES),
            'payments': copy.deepcopy(PAYMENT_SAMPLES),
        }

        self.create_users(self.samples['users'])
        self.create_admins(self.samples['admins'])

        self.create_funds(self.samples['funds'])
        for sample in self.samples['genres'].values():
            key = sample['fund']['key']
            sample['fund']['id'] = self.samples['funds'][key]['id']
            sample['fund'].pop('key', None)

        self.create_genres(self.samples['genres'])
        for sample in self.samples['payments'].values():
            key = sample['fund']['key']
            sample['fund']['id'] = self.samples['funds'][key]['id']
            sample['fund'].pop('key', None)

            key = sample['genre']['key']
            sample['genre']['id'] = self.samples['genres'][key]['id']
            sample['genre'].pop('key', None)
