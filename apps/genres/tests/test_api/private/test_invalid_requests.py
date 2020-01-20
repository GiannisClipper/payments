from unittest import skip  # noqa: F401
from rest_framework import status

from genres.tests.test_api import ROOT_URL, BY_ID_1_URL, LIST_URL

from . import AdminPrivateGenresAPITests, OwnerPrivateGenresAPITests

from genres.constants import (
    USER_REQUIRED,
    CODE_REQUIRED,
    NAME_REQUIRED,
    CODE_EXISTS,
    NAME_EXISTS,
    FUND_INVALID,
)


class AdminPost(AdminPrivateGenresAPITests):
    '''Test admin's invalid POST requests to funds API.'''

    METHOD = 'POST'

    def test_when_values_are_missing(self):
        sample = {}

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(3, len(res.data['errors']))
        self.assertIn(USER_REQUIRED, res.data['errors']['user'])
        self.assertIn(CODE_REQUIRED, res.data['errors']['code'])
        self.assertIn(NAME_REQUIRED, res.data['errors']['name'])
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_exists(self):
        sample = self.samples['genres'][11]
        self.create_genre(**sample)

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(2, len(res.data['errors']))
        self.assertIn(CODE_EXISTS, res.data['errors']['code'])
        self.assertIn(NAME_EXISTS, res.data['errors']['name'])
        self.assertEqual(res.data['token'], self.token)

    def test_when_fund_user_is_invalid(self):
        sample = self.samples['genres'][11]
        sample['fund']['id'] = self.samples['funds'][21]['id']
        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('fund', res.data['errors'])
        self.assertEqual(FUND_INVALID, res.data['errors']['fund'])
        self.assertEqual(1, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)


class AdminGet(AdminPrivateGenresAPITests):
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

    def test_when_values_are_empty(self):
        sample = self.samples['genres'][11]
        self.create_genre(**sample)
        sample = {'user': None, 'code': None, 'name': None}

        res = self.api_request(BY_ID_1_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(3, len(res.data['errors']))
        self.assertIn(USER_REQUIRED, res.data['errors']['user'])
        self.assertIn(CODE_REQUIRED, res.data['errors']['code'])
        self.assertIn(NAME_REQUIRED, res.data['errors']['name'])
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_exists(self):
        sample = self.samples['genres'][11]
        self.create_genre(**sample)
        sample = self.samples['genres'][12]
        self.create_genre(**sample)
        sample.pop('user', None)

        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(2, len(res.data['errors']))
        self.assertIn(CODE_EXISTS, res.data['errors']['code'])
        self.assertIn(NAME_EXISTS, res.data['errors']['name'])
        self.assertEqual(res.data['token'], self.token)


class AdminDelete(AdminGet):
    '''Test admin's invalid DELETE requests to funds API.'''

    METHOD = 'DELETE'

    # To be executed the inherited tests


class OwnerPost(OwnerPrivateGenresAPITests, AdminPost):
    '''Test owner's invalid POST requests to funds API.'''

    def test_when_values_are_missing(self):
        sample = {}

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        # No check for `user` in errors, automatically gets the owner
        self.assertIn('code', res.data['errors'])
        self.assertIn('name', res.data['errors'])
        self.assertEqual(2, len(res.data['errors']))
        self.assertIn(CODE_REQUIRED, res.data['errors']['code'])
        self.assertIn(NAME_REQUIRED, res.data['errors']['name'])
        self.assertEqual(res.data['token'], self.token)


class OwnerGet(OwnerPrivateGenresAPITests, AdminGet):
    '''Test owner's invalid GET requests to funds API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        sample = self.samples['genres'][21]  # not equal to id of signed user
        self.create_genre(**sample)

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


class AdminGetList(AdminPrivateGenresAPITests):
    '''Test admin's invalid GET requests to funds API.'''

    METHOD = 'GET'

    def test_request_when_user_id_not_exists(self):
        res = self.api_request(LIST_URL + '?filters=user_id:blabla', self.METHOD, token=self.token)  # noqa: E501

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerGetList(OwnerPrivateGenresAPITests):
    '''Test owner's invalid list requests to funds API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        res = self.api_request(LIST_URL + '?filters=user_id:blabla', self.METHOD, token=self.token)  # noqa: E501

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)
