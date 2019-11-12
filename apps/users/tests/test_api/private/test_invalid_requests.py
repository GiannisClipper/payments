from django.urls import reverse
from rest_framework import status

from . import OwnerSigninSupported, AdminSigninSupported

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
    INPUT_NOT_MATCH,
)

BY_ID_1_URL = reverse('users:by-id', kwargs={'id': 1})
BY_ID_2_URL = reverse('users:by-id', kwargs={'id': 2})
BY_ID_0_URL = reverse('users:by-id', kwargs={'id': 0})

CURRENT_URL = reverse('users:current')


class AdminGetUserByIdAPITests(AdminSigninSupported):
    '''Test admin's invalid GET requests to users API.'''

    URL = BY_ID_2_URL

    METHOD = 'GET'

    def test_when_id_not_exists(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        res = self.api_request(BY_ID_0_URL, self.METHOD, token=token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class AdminPatchUserByIdAPITests(AdminGetUserByIdAPITests):
    '''Test admin's invalid PATCH requests to users API.'''

    METHOD = 'PATCH'

    def test_when_values_exists_or_invalid(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        sample = self.samples['users'][3]
        sample['password'] = '*'
        res = self.api_request(self.URL, self.METHOD, payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_when_values_are_empty(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        sample['username'] = ''
        sample['password'] = ''
        sample['email'] = None
        res = self.api_request(self.URL, self.METHOD, payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])


class AdminDeleteUserByIdAPITests(AdminGetUserByIdAPITests):
    '''Test admin's invalid DELETE requests to users API.'''

    METHOD = 'DELETE'

    def test_when_not_authenticate_well(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        sample['password'] = 'blabla'
        res = self.api_request(self.URL, self.METHOD, payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors'])
        self.assertEqual(token, res.data['token'])


class OwnerGetUserByIdAPITests(OwnerSigninSupported, AdminGetUserByIdAPITests):
    '''Test owner's invalid GET requests to users API.'''

    URL = BY_ID_1_URL

    METHOD = 'GET'

    def test_unauthorized_request(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        res = self.api_request(BY_ID_2_URL, self.METHOD, token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class OwnerPatchUserByIdAPITests(OwnerGetUserByIdAPITests, AdminPatchUserByIdAPITests):
    '''Test owner's invalid PATCH requests to users API.'''

    METHOD = 'PATCH'


class OwnerDeleteUserByIdAPITests(OwnerGetUserByIdAPITests, AdminDeleteUserByIdAPITests):
    '''Test owner's invalid DELETE requests to users API.'''

    METHOD = 'DELETE'


class OwnerGetCurrentUserAPITests(OwnerGetUserByIdAPITests):
    '''Test owner's invalid GET requests to users API.'''

    URL = CURRENT_URL


class OwnerPatchCurrentUserAPITests(OwnerPatchUserByIdAPITests):
    '''Test owner's invalid PATCH requests to users API.'''

    URL = CURRENT_URL


class OwnerDeleteCurrentUserAPITests(OwnerDeleteUserByIdAPITests):
    '''Test owner's invalid DELETE requests to users API.'''

    URL = CURRENT_URL


class OwnerGetListAPITests(OwnerSigninSupported):
    '''Test all users list API.'''

    LIST_URL = reverse('users:all-list')

    def test_unauthorized_request(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        res = self.api_request(self.LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class OwnerGetAdminUsersListAPITests(OwnerGetListAPITests):
    '''Test admin users list API.'''

    LIST_URL = reverse('users:admin-list')


class OwnerGetNoAdminUsersListAPITests(OwnerGetListAPITests):
    '''Test no admin users (simple users) list API.'''

    LIST_URL = reverse('users:no-admin-list')


class OwnerGetActiveUsersListAPITests(OwnerGetListAPITests):
    '''Test active users list API.'''

    LIST_URL = reverse('users:active-list')


class OwnerGetNoActiveUsersListAPITests(OwnerGetListAPITests):
    '''Test no active users (simple users) list API.'''

    LIST_URL = reverse('users:no-active-list')
