from unittest import skip  # noqa: F401
from rest_framework import status

from payments.tests.test_api import ROOT_URL, BY_ID_1_URL, LIST_URL

from . import AdminPrivatePaymentsAPITests, OwnerPrivatePaymentsAPITests


class AdminPost(AdminPrivatePaymentsAPITests):
    '''Test admin's invalid POST requests to payments API.'''

    METHOD = 'POST'

    def test_when_values_exists(self):
        sample = self.samples['payments'][11]
        self.create_payment(**sample)

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('__all__', res.data['errors'])
        self.assertEqual(1, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_are_missing(self):
        sample = {}

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('date', res.data['errors'])
        self.assertIn('genre', res.data['errors'])
        self.assertIn('fund', res.data['errors'])
        self.assertEqual(4, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)

    def test_when_invalid_genre_user_or_fund_user(self):
        sample = self.samples['payments'][11]
        sample['genre']['id'] = self.samples['genres'][21]['id']
        sample['fund']['id'] = self.samples['funds'][21]['id']
        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('genre', res.data['errors'])
        self.assertIn('fund', res.data['errors'])
        self.assertEqual(2, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)


class AdminGet(AdminPrivatePaymentsAPITests):
    '''Test admin's invalid GET requests to payments API.'''

    METHOD = 'GET'

    def test_request_when_id_not_exists(self):
        res = self.api_request(BY_ID_1_URL, self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class AdminPatch(AdminGet):
    '''Test admin's invalid PATCH requests to payments API.'''

    METHOD = 'PATCH'

    def test_when_values_exists(self):
        sample = self.samples['payments'][11]
        self.create_payment(**sample)
        sample = self.samples['payments'][12]
        self.create_payment(**sample)

        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('__all__', res.data['errors'])
        self.assertEqual(1, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)

    def test_when_values_are_empty(self):
        sample = self.samples['payments'][11]
        self.create_payment(**sample)
        sample = {
            'user': None, 'date': None, 'genre': None,
            'incoming': None, 'outgoing': None, 'fund': None, 'remarks': None
        }

        res = self.api_request(BY_ID_1_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('user', res.data['errors'])
        self.assertIn('date', res.data['errors'])
        self.assertIn('genre', res.data['errors'])
        self.assertIn('fund', res.data['errors'])
        self.assertEqual(4, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)


class AdminDelete(AdminGet):
    '''Test admin's invalid DELETE requests to payments API.'''

    METHOD = 'DELETE'

    # To be executed the inherited tests


class OwnerPost(OwnerPrivatePaymentsAPITests, AdminPost):
    '''Test owner's invalid POST requests to payments API.'''

    def test_when_values_are_missing(self):
        sample = {}

        res = self.api_request(ROOT_URL, self.METHOD, payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        # No check for `user` in errors, automatically gets the owner
        self.assertIn('date', res.data['errors'])
        self.assertIn('genre', res.data['errors'])
        self.assertIn('fund', res.data['errors'])
        self.assertEqual(3, len(res.data['errors']))
        self.assertEqual(res.data['token'], self.token)


class OwnerGet(OwnerPrivatePaymentsAPITests, AdminGet):
    '''Test owner's invalid GET requests to payments API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        sample = self.samples['payments'][21]  # not equal to id of signed user
        self.create_payment(**sample)

        res = self.api_request(BY_ID_1_URL, self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerPatch(OwnerGet, AdminPatch):
    '''Test owner's invalid PATCH requests to payments API.'''

    METHOD = 'PATCH'


class OwnerDelete(OwnerGet, AdminDelete):
    '''Test owner's invalid DELETE requests to payments API.'''

    METHOD = 'DELETE'


class AdminGetList(AdminPrivatePaymentsAPITests):
    '''Test admin's invalid GET requests to payments API.'''

    METHOD = 'GET'

    def test_request_when_user_id_not_exists(self):
        res = self.api_request(LIST_URL + '?user_id=blabla', self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerGetList(OwnerPrivatePaymentsAPITests):
    '''Test owner's invalid list requests to payments API.'''

    METHOD = 'GET'

    def test_unauthorized_request(self):
        res = self.api_request(LIST_URL + '?user_id=blabla', self.METHOD, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(res.data['token'], self.token)
