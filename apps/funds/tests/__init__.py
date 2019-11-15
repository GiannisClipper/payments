from django.test import TestCase

import copy

from django.contrib.auth import get_user_model

from funds.models import Fund

from users.tests import UserCreateMethods
from users.tests import USER_SAMPLES, ADMIN_SAMPLES

FUND_SAMPLES = {
    # First key digit is equal to user id

    11: {'user': {'id': 1}, 'code': '1', 'name': 'CASH'},
    12: {'user': {'id': 1}, 'code': '2', 'name': 'VISA'},
    13: {'user': {'id': 1}, 'code': '3', 'name': 'MASTERCARD'},
    21: {'user': {'id': 2}, 'code': '1', 'name': 'CASH'},
    22: {'user': {'id': 2}, 'code': '2', 'name': 'PREPAID CARD'},
}


class FundCreateMethods:

    def create_fund(self, **fund):
        fund['user'] = get_user_model().objects.get(pk=fund['user']['id'])

        return Fund.objects.create(**fund)


    def create_funds(self, samples):
        for fund in samples.values():
            self.create_fund(**fund)


class FundsTests(TestCase, FundCreateMethods, UserCreateMethods):

    def setUp(self):
        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'admins': copy.deepcopy(ADMIN_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
        }

        self.create_users(self.samples['users'])
        self.create_admins(self.samples['admins'])
