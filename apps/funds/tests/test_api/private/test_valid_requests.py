from rest_framework import status

from funds.tests.test_api import ROOT_URL, BY_ID_1_URL

from . import OwnerPrivateFundsAPITests, AdminPrivateFundsAPITests


class OwnerRequest(OwnerPrivateFundsAPITests):
    '''Test owner's valid requests to funds API.'''

    def test_post(self):
        sample = self.samples['funds'][0]
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['username'], self.user.username)
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertIn(f"/funds/{res.data['fund']['id']}/", res.data['fund']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_get(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)
        res = self.api_request(BY_ID_1_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['username'], self.user.username)
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertIn(f"/funds/{res.data['fund']['id']}/", res.data['fund']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_patch(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)
        sample = self.samples['funds'][1]
        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertEqual(res.data['token'], self.token)

    def test_delete(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)
        res = self.api_request(BY_ID_1_URL, 'DELETE', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund'], {})
        self.assertEqual(res.data['token'], self.token)


class AdminRequest(AdminPrivateFundsAPITests):
    '''Test admin's valid requests to funds API.'''

    def test_post_same_values_to_other_user(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)  # admin who has signed in
        sample['user'] = self.user2.pk  # same values to other user
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['username'], self.user2.username)
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertIn(f"/funds/{res.data['fund']['id']}/", res.data['fund']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_get(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user2, sample)  # other user
        res = self.api_request(BY_ID_1_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['username'], self.user2.username)
        self.assertEqual(res.data['fund']['code'], sample['code'])
        self.assertEqual(res.data['fund']['name'], sample['name'])
        self.assertIn(f"/funds/{res.data['fund']['id']}/", res.data['fund']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_patch_values_to_other_user(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)  # admin who has signed in
        sample['user'] = self.user2.pk  # other user
        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund']['user']['username'], self.user2.username)
        self.assertEqual(res.data['token'], self.token)

    def test_delete(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user2, sample)  # other user
        res = self.api_request(BY_ID_1_URL, 'DELETE', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('fund', res.data)
        self.assertEqual(res.data['fund'], {})
        self.assertEqual(res.data['token'], self.token)
