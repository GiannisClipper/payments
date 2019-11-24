from unittest import skip  # noqa: F401
from django.urls import reverse
from rest_framework import status

from . import UsersPrivateAPITests

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
    CREDENTIALS_NOT_MATCH,
)

BY_ID_1_URL = reverse('users:by-id', kwargs={'id': 1})  # first admin id
BY_ID_3_URL = reverse('users:by-id', kwargs={'id': 3})  # first owner id
BY_ID_0_URL = reverse('users:by-id', kwargs={'id': 0})  # id not exists

CURRENT_URL = reverse('users:current')


class AdminGetUserByIdAPITests(UsersPrivateAPITests):
    '''Test admin's invalid GET requests to users API.'''

    URL = BY_ID_3_URL

    METHOD = 'GET'

    def setUp(self):
        super().setUp()
        self.SIGNIN_USER = self.samples['admins'][1]

    def test_when_id_not_exists(self):
        sample = self.SIGNIN_USER
        user, token = self.signin(sample)
        res = self.api_request(BY_ID_0_URL, self.METHOD, token=token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class AdminPatchUserByIdAPITests(AdminGetUserByIdAPITests):
    '''Test admin's invalid PATCH requests to users API.'''

    METHOD = 'PATCH'

    def test_when_values_exists_or_invalid(self):
        sample = self.SIGNIN_USER
        user, token = self.signin(sample)
        sample = self.samples['admins'][2]
        sample['password'] = '*'
        res = self.api_request(self.URL, self.METHOD, payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('username', res.data['errors'])
        self.assertIn('password', res.data['errors'])
        self.assertIn('email', res.data['errors'])
        self.assertEqual(3, len(res.data['errors']))
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_when_values_are_empty(self):
        sample = self.SIGNIN_USER
        user, token = self.signin(sample)
        sample['username'] = ''
        sample['password'] = ''
        sample['email'] = None
        res = self.api_request(self.URL, self.METHOD, payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn('username', res.data['errors'])
        self.assertIn('password', res.data['errors'])
        self.assertIn('email', res.data['errors'])
        self.assertEqual(3, len(res.data['errors']))
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])


class AdminDeleteUserByIdAPITests(AdminGetUserByIdAPITests):
    '''Test admin's invalid DELETE requests to users API.'''

    METHOD = 'DELETE'

    def test_when_not_authenticate_well(self):
        sample = self.SIGNIN_USER
        user, token = self.signin(sample)
        sample['password'] = 'blabla'
        res = self.api_request(self.URL, self.METHOD, payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(CREDENTIALS_NOT_MATCH, res.data['errors'])
        self.assertEqual(token, res.data['token'])


class OwnerGetUserByIdAPITests(AdminGetUserByIdAPITests):
    '''Test owner's invalid GET requests to users API.'''

    def setUp(self):
        super().setUp()
        self.SIGNIN_USER = self.samples['users'][1]

    def test_unauthorized_request(self):
        sample = self.SIGNIN_USER
        user, token = self.signin(sample)
        res = self.api_request(BY_ID_1_URL, self.METHOD, token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class OwnerPatchUserByIdAPITests(OwnerGetUserByIdAPITests, AdminPatchUserByIdAPITests):
    '''Test owner's invalid PATCH requests to users API.'''


class OwnerDeleteUserByIdAPITests(OwnerGetUserByIdAPITests, AdminDeleteUserByIdAPITests):
    '''Test owner's invalid DELETE requests to users API.'''


class OwnerGetCurrentUserAPITests(OwnerGetUserByIdAPITests):
    '''Test owner's invalid GET requests to users API.'''

    URL = CURRENT_URL


class OwnerPatchCurrentUserAPITests(OwnerPatchUserByIdAPITests):
    '''Test owner's invalid PATCH requests to users API.'''

    URL = CURRENT_URL


class OwnerDeleteCurrentUserAPITests(OwnerDeleteUserByIdAPITests):
    '''Test owner's invalid DELETE requests to users API.'''

    URL = CURRENT_URL


class OwnerGetListAPITests(UsersPrivateAPITests):
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
