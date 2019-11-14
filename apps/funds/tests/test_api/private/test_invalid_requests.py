from unittest import skip  # noqa: F401
from rest_framework import status

from funds.tests.test_api import ROOT_URL, BY_ID_1_URL, LIST_URL

from . import AdminPrivateFundsAPITests, OwnerPrivateFundsAPITests


class AdminPost(AdminPrivateFundsAPITests):
    '''Test admin's invalid POST requests to funds API.'''

    METHOD = 'POST'

    def test_when_values_exists(self):
        sample = self.samples['funds'][1]
        self.create_fund(**sample)
        self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_are_missing(self):
        sample = {}

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)


class AdminGet(AdminPrivateFundsAPITests):
    '''Test admin's invalid GET requests to funds API.'''

    METHOD = 'GET'

    def test_request_when_id_not_exists(self):
        res = self.api_request(BY_ID_1_URL, self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class AdminPatch(AdminGet):
    '''Test admin's invalid PATCH requests to funds API.'''

    METHOD = 'PATCH'

    def test_when_values_exists(self):
        sample = self.samples['funds'][1]
        self.create_fund(**sample)
        sample = self.samples['funds'][2]
        self.create_fund(**sample)
        sample.pop('user', None)

        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_are_empty(self):
        sample = self.samples['funds'][1]
        self.create_fund(**sample)
        sample = {'user': None, 'code': None, 'name': None}

        res = self.api_request(BY_ID_1_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)


class AdminDelete(AdminGet):
    '''Test admin's invalid DELETE requests to funds API.'''

    METHOD = 'DELETE'

    # To be executed the inherited tests


class OwnerPost(OwnerPrivateFundsAPITests, AdminPost):
    '''Test owner's invalid POST requests to funds API.'''

    def test_when_values_are_missing(self):
        sample = {}

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        # No check for `user` in errors, automatically gets the owner
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(res.data['token'], self.token)


class OwnerGet(OwnerPrivateFundsAPITests, AdminGet):
    '''Test owner's invalid GET requests to funds API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        sample = self.samples['funds'][1]
        sample['user']['id'] = self.user['id'] + 1  # not equal to id of signed user
        self.create_fund(**sample)

        res = self.api_request(BY_ID_1_URL, self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerPatch(OwnerGet, AdminPatch):
    '''Test owner's invalid PATCH requests to funds API.'''

    METHOD = 'PATCH'


class OwnerDelete(OwnerGet, AdminDelete):
    '''Test owner's invalid DELETE requests to funds API.'''

    METHOD = 'DELETE'


class AdminGetList(AdminPrivateFundsAPITests):
    '''Test admin's invalid GET requests to funds API.'''

    METHOD = 'GET'

    def test_request_when_user_id_not_exists(self):
        res = self.api_request(LIST_URL + '?user_id=blabla', self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerGetList(OwnerPrivateFundsAPITests):
    '''Test owner's invalid list requests to funds API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        res = self.api_request(LIST_URL + '?user_id=blabla', self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)
