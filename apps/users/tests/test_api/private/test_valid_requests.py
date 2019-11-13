from django.urls import reverse
from rest_framework import status

from . import UsersPrivateAPITests

BY_ID_1_URL = reverse('users:by-id', kwargs={'id': 1})  # first admin id
BY_ID_3_URL = reverse('users:by-id', kwargs={'id': 3})  # first owner id
BY_ID_0_URL = reverse('users:by-id', kwargs={'id': 0})  # id not exists

CURRENT_URL = reverse('users:current')


class AdminRequestUserByIdAPITests(UsersPrivateAPITests):
    '''Test user-by-id API by admin.'''

    def test_get(self):
        sample = self.samples['admins'][1]
        user, token = self.signin(sample)
        res = self.api_request(BY_ID_3_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user['username'], res.data['user']['username'])
        self.assertIn(f"/users/{res.data['user']['id']}/", res.data['user']['url'])
        self.assertEqual(token, res.data['token'])

    def test_patch(self):
        sample = self.samples['admins'][1]
        user, token = self.signin(sample)
        sample['username'] += 'blabla'
        sample['email'] += 'blabla'
        res = self.api_request(BY_ID_3_URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user['id'], res.data['user']['id'])
        self.assertEqual(sample['username'], res.data['user']['username'])
        self.assertEqual(sample['email'], res.data['user']['email'])
        self.assertEqual(token, res.data['token'])

    def test_delete(self):
        sample = self.samples['admins'][1]
        user, token = self.signin(sample)
        res = self.api_request(BY_ID_3_URL, 'DELETE', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual({}, res.data['user'])
        self.assertEqual(token, res.data['token'])


class OwnerRequestUserByIdAPITests(UsersPrivateAPITests):
    '''Test user-by-id API by owner.'''

    URL = BY_ID_3_URL

    def test_get(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        res = self.api_request(self.URL, 'GET', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user['username'], res.data['user']['username'])
        self.assertEqual(token, res.data['token'])

    def test_patch(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        sample['username'] += 'blabla'
        sample['email'] += 'blabla'
        res = self.api_request(self.URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user['id'], res.data['user']['id'])
        self.assertEqual(sample['username'], res.data['user']['username'])
        self.assertEqual(sample['email'], res.data['user']['email'])
        self.assertEqual(token, res.data['token'])

    def test_delete(self):
        sample = self.samples['users'][1]
        user, token = self.signin(sample)
        res = self.api_request(self.URL, 'DELETE', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual({}, res.data['user'])
        self.assertEqual(token, res.data['token'])


class CurrentUserAPITests(OwnerRequestUserByIdAPITests):
    '''Test current user API.'''

    URL = CURRENT_URL


class AdmninGetListAPITests(UsersPrivateAPITests):
    '''Test all users list API.'''

    LIST_URL = reverse('users:all-list')

    def test_get(self):
        sample = self.samples['admins'][1]
        user, token = self.signin(sample)
        res = self.api_request(self.LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('users', res.data)
        self.assertTrue(isinstance(res.data['users'], list))
        self.assertEqual(token, res.data['token'])


class AdmninGetAdminUsersListAPITests(AdmninGetListAPITests):
    '''Test admin users list API.'''

    LIST_URL = reverse('users:admin-list')


class AdmninGetNoAdminUsersListAPITests(AdmninGetListAPITests):
    '''Test no admin users (simple users) list API.'''

    LIST_URL = reverse('users:no-admin-list')


class AdmninGetActiveUsersListAPITests(AdmninGetListAPITests):
    '''Test active users list API.'''

    LIST_URL = reverse('users:active-list')


class AdmninGetNoActiveUsersListAPITests(AdmninGetListAPITests):
    '''Test no active users (simple users) list API.'''

    LIST_URL = reverse('users:no-active-list')
