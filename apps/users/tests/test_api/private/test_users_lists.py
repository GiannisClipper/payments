from . import PrivateUsersAPITests

from django.urls import reverse

from rest_framework import status


class AllUsersListAPITests(PrivateUsersAPITests):
    '''Test all users list API.'''

    LIST_URL = reverse('users:all-list')

    def test_retrieve(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        res = self.api_request(self.LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('users', res.data)
        self.assertTrue(isinstance(res.data['users'], list))
        self.assertEqual(token, res.data['token'])

    def test_invalid_retrieve_without_permission(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
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
