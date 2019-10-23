from rest_framework import status

from funds.tests.test_api import ROOT_URL, BY_ID_1_URL

from . import OwnerPrivateFundsAPITests, AdminPrivateFundsAPITests


class OwnerGetRequestsFundsAPI(OwnerPrivateFundsAPITests):
    '''Test owner's invalid GET requests to funds API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user2, sample)
        res = self.api_request(BY_ID_1_URL, self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)

    def test_request_when_id_not_exists(self):
        res = self.api_request(BY_ID_1_URL, self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerPostRequestsFundsAPI(OwnerPrivateFundsAPITests):
    '''Test owner's invalid POST requests to funds API.'''

    METHOD = 'POST'

    def test_when_values_exists(self):
        sample = self.samples['funds'][0]
        self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_are_missing(self):
        sample = {}
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)


class OwnerPatchRequestsFundsAPI(OwnerGetRequestsFundsAPI):
    '''Test owner's invalid PATCH requests to funds API.'''

    METHOD = 'PATCH'

    def test_when_values_exists(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)
        sample = self.samples['funds'][1]
        self.create_fund(self.user, sample)
        sample.pop('user', None)
        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_are_empty(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)
        sample = {'user': None, 'code': None, 'name': None}
        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)


class OwnerDeleteRequestsFundsAPI(OwnerGetRequestsFundsAPI):
    '''Test owner's invalid DELETE requests to funds API.'''

    METHOD = 'DELETE'


class AdminRequestsFundsAPI(AdminPrivateFundsAPITests):
    '''Test admin's invalid requests to funds API.'''

    def test_post_when_values_are_missing(self):
        sample = {}
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)

    def test_patch_when_values_are_empty(self):
        sample = self.samples['funds'][0]
        self.create_fund(self.user, sample)
        sample = {'user': None, 'code': None, 'name': None}
        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)
