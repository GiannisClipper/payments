from . import PrivateUsersAPITests

from django.urls import reverse

from rest_framework import status

from .test_current_user import CurrentUserAPITests

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


class OwnerAccessUserByIdAPITests(CurrentUserAPITests):
    '''Test user-by-id API by owner.'''

    URL = BY_ID_1_URL


class AdminAccessUserByIdAPITests(PrivateUsersAPITests):
    '''Test user-by-id API by admin.'''

    def test_valid_retrieve(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        res = self.api_request(BY_ID_2_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user['username'], res.data['user']['username'])
        self.assertIn(f"/users/{res.data['user']['id']}/", res.data['user']['url'])
        self.assertEqual(token, res.data['token'])

    def test_valid_update(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        sample['username'] += 'blabla'
        sample['email'] += 'blabla'
        res = self.api_request(BY_ID_2_URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user['id'], res.data['user']['id'])
        self.assertEqual(sample['username'], res.data['user']['username'])
        self.assertEqual(sample['email'], res.data['user']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_exists_or_invalid(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        sample['password'] = '*'
        res = self.api_request(BY_ID_2_URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_are_empty(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        sample['username'] = ''
        sample['password'] = ''
        sample['email'] = None
        res = self.api_request(BY_ID_2_URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_valid_delete(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        res = self.api_request(BY_ID_2_URL, 'DELETE', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual({}, res.data['user'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_delete_when_not_authenticate_well(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        sample['password'] = 'blabla'
        res = self.api_request(BY_ID_2_URL, 'DELETE', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors'])
        self.assertEqual(token, res.data['token'])


class PostUserByIdWhenNotAccessible(PrivateUsersAPITests):
    '''Test POST user-by-id API when it should/ could not accessed.'''

    METHOD = 'Post'

    def test_invalid_request_without_permission(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        res = self.api_request(BY_ID_2_URL, self.METHOD, token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])

    def test_invalid_request_when_id_not_exists(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_admin(sample)
        res = self.api_request(BY_ID_0_URL, self.METHOD, token=token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class GetUserByIdWhenNotAccessible(PostUserByIdWhenNotAccessible):
    '''Test GET user-by-id API when it should/ could not accessed'''

    METHOD = 'GET'


class PatchUserByIdWhenNotAccessible(PostUserByIdWhenNotAccessible):
    '''Test PATCH user-by-id API when it should/ could not accessed'''

    METHOD = 'PATCH'


class DeleteUserByIdWhenNotAccessible(PostUserByIdWhenNotAccessible):
    '''Test DELETE user-by-id API when it should/ could not accessed'''

    METHOD = 'DELETE'
