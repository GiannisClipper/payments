from django.test import TestCase

import copy

from django.contrib.auth import get_user_model

from funds.models import Fund

from users.tests import UserCreateMethods
from users.tests import USER_SAMPLES, ADMIN_SAMPLES

FUND_SAMPLES = {
    # First dict key digit is equal to user dict key

    11: {'user': {'id': 1}, 'code': '1', 'name': 'CASH'},
    12: {'user': {'id': 1}, 'code': '2', 'name': 'VISA'},
    13: {'user': {'id': 1}, 'code': '3', 'name': 'MASTERCARD'},
    21: {'user': {'id': 2}, 'code': '1', 'name': 'CASH'},
    22: {'user': {'id': 2}, 'code': '2', 'name': 'PREPAID CARD'},
}


class FundCreateMethods:

    def create_fund(self, **sample):
        sample['user'] = get_user_model().objects.get(pk=sample['user']['id'])
        fund = Fund.objects.create(**sample)

        return fund

    def create_funds(self, samples):
        for sample in samples.values():
            fund = self.create_fund(**sample)
            sample['id'] = fund.pk


class FundsTests(TestCase, FundCreateMethods, UserCreateMethods):

    def setUp(self):
        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES),
            'admins': copy.deepcopy(ADMIN_SAMPLES),
            'funds': copy.deepcopy(FUND_SAMPLES),
        }

        self.create_users(self.samples['users'])
        self.create_admins(self.samples['admins'])
