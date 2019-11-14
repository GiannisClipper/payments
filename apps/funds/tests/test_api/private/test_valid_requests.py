from unittest import skip  # noqa: F401
from rest_framework import status

from funds.tests.test_api import ROOT_URL, BY_ID_1_URL, LIST_URL

from . import AdminPrivateFundsAPITests, OwnerPrivateFundsAPITests


class AdminRequests(AdminPrivateFundsAPITests):
    '''Test admin's valid requests to funds API.'''

    # Signed admin has id > 1 other than owner's id in samples (funds)

    def test_post(self):
        sample = self.samples['funds'][1]

        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['id'], sample['user']['id'])
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertIn(f"/funds/{res.data['fund']['id']}/", res.data['fund']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_get(self):
        sample = self.samples['funds'][1]
        self.create_fund(**sample)

        res = self.api_request(BY_ID_1_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['id'], sample['user']['id'])
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertIn(f"/funds/{res.data['fund']['id']}/", res.data['fund']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_patch(self):
        sample = self.samples['funds'][1]
        self.create_fund(**sample)
        sample = self.samples['funds'][2]

        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['id'], sample['user']['id'])
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertEqual(res.data['token'], self.token)

    def test_delete(self):
        sample = self.samples['funds'][1]
        self.create_fund(**sample)

        res = self.api_request(BY_ID_1_URL, 'DELETE', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund'], {})
        self.assertEqual(res.data['token'], self.token)


class OwnerRequests(OwnerPrivateFundsAPITests, AdminRequests):
    '''Test owner's valid requests to funds API.'''

    # Signed user has id = 1 same with owner's id in samples (funds)


class AdminGetList(AdminPrivateFundsAPITests):
    '''Test admin's list requests to funds API.'''

    def setUp(self):
        super().setUp()
        self.create_funds(self.samples['funds'])

    def test_get_list(self):
        res = self.api_request(LIST_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('funds', res.data)
        self.assertEqual(len(res.data['funds']), len(self.samples['funds']))
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_other_user_id(self):
        res = self.api_request(LIST_URL + '?user_id=1', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('funds', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerGetList(OwnerPrivateFundsAPITests):
    '''Test owner's list requests to funds API.'''

    def setUp(self):
        super().setUp()
        self.create_funds(self.samples['funds'])

    def test_get_list(self):
        res = self.api_request(LIST_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('funds', res.data)
        self.assertNotEqual(len(res.data['funds']), len(self.samples['funds']))
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_self_user_id(self):
        res = self.api_request(LIST_URL + '?user_id=1', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('funds', res.data)
        self.assertEqual(res.data['token'], self.token)
