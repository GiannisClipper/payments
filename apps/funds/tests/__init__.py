from django.test import TestCase

import copy

from funds.models import Fund

from users.tests import SAMPLES as USERS_SAMPLES

SAMPLES = [
    [
        {'code': '1', 'name': 'CASH'},
        {'code': '2', 'name': 'VISA'},
        {'code': '3', 'name': 'MASTERCARD'},
    ],
    [
        {'code': '1', 'name': 'CASH'},
        {'code': '2', 'name': 'PREPAID CARD'},
    ],
]


class FundsTests(TestCase):

    def setUp(self):

        self.samples = {
            'users': copy.deepcopy(USERS_SAMPLES),
            'funds': copy.deepcopy(SAMPLES),
        }

    @staticmethod
    def create_fund(user, fund):

        fund['user'] = user

        return Fund.objects.create(**fund)
