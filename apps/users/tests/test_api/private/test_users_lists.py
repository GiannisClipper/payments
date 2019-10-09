from . import PrivateUsersAPITests

from django.urls import reverse

from rest_framework import status


class AllUsersListAPITests(PrivateUsersAPITests):
    '''Test all users list API.'''

    LIST_URL = reverse('users:all-list')

    def setUp(self):
        super().setUp()

        # self.create_user(**self.samples[0]) takes over through `signin()`
        # self.create_user(**self.samples[1]) takes over through `signin()`
        self.create_user(**self.samples[2])
        self.create_user(**self.samples[3])
        self.create_admin(**self.samples[4])

    def test_retrieve_(self):
        user, token = self.signin_as_admin()
        res = self.api_request(self.LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('users', res.data)
        self.assertTrue(type(res.data['users']) == list)
        self.assertEqual(token, res.data['token'])

    def test_invalid_retrieve_without_permission(self):
        user, token = self.signin()
        res = self.api_request(self.LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class AdminUsersListAPITests(AllUsersListAPITests):
    '''Test admin users list API.'''

    LIST_URL = reverse('users:admin-list')


class NoAdminUsersListAPITests(AllUsersListAPITests):
    '''Test no admin users (simple users) list API.'''

    LIST_URL = reverse('users:no-admin-list')


class ActiveUsersListAPITests(AllUsersListAPITests):
    '''Test active users list API.'''

    LIST_URL = reverse('users:active-list')


class NoActiveUsersListAPITests(AllUsersListAPITests):
    '''Test no active users (simple users) list API.'''

    LIST_URL = reverse('users:no-active-list')
