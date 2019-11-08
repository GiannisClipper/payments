from django.test import TestCase

import copy

from funds.models import Fund

from users.tests import UserCreateMethods
from users.tests import USER_SAMPLES

FUND_SAMPLES = [
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


class FundCreateMethods:

    def create_fund(self, user, fund):
        fund['user'] = user

        return Fund.objects.create(**fund)


class FundsTests(TestCase, FundCreateMethods, UserCreateMethods):

    def setUp(self):
        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
        }
