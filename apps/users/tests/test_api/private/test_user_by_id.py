from . import PrivateUsersAPITests

from django.urls import reverse

from rest_framework import status

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
    INPUT_NOT_MATCH,
)

BY_ID_2_URL = reverse('users:byid', kwargs={'id': 2})
BY_ID_3_URL = reverse('users:byid', kwargs={'id': 3})


class UserByIdWithoutPermissionAPITests(PrivateUsersAPITests):
    '''Test user by id API whithout auth permission.'''

    def request_without_permission(self, method):
        user, token = self.signin()
        res = self.api_request(BY_ID_2_URL, method, token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])

    def test_invalid_retrieve_without_permission(self):
        self.request_without_permission(method='GET')

    def test_invalid_update_without_permission(self):
        self.request_without_permission(method='PATCH')

    def test_invalid_delete_without_permission(self):
        self.request_without_permission(method='DELETE')


class UserByIdWhenNotFoundAPITests(PrivateUsersAPITests):
    '''Test user by id API when id not found.'''

    def request_an_id_that_not_exists(self, method):
        user, token = self.signin_as_admin()
        res = self.api_request(BY_ID_3_URL, method, token=token)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])

    def test_invalid_retrieve_when_not_found(self):
        self.request_an_id_that_not_exists(method='GET')

    def test_invalid_update_when_not_found(self):
        self.request_an_id_that_not_exists(method='PATCH')

    def test_invalid_delete_when_not_found(self):
        self.request_an_id_that_not_exists(method='DELETE')


class UserByIdAPITests(PrivateUsersAPITests):
    '''Test user by id API.'''

    def test_valid_retrieve(self):
        user, token = self.signin_as_admin()
        res = self.api_request(BY_ID_2_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user['username'], res.data['user']['username'])
        self.assertIn(
            f"/users/{res.data['user']['id']}/", res.data['user']['url']
        )
        self.assertEqual(token, res.data['token'])

    def test_valid_update(self):
        user, token = self.signin_as_admin()
        payload = self.samples[2]
        res = self.api_request(
            BY_ID_2_URL, 'PATCH', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user['id'], res.data['user']['id'])
        self.assertEqual(payload['username'], res.data['user']['username'])
        self.assertEqual(payload['email'], res.data['user']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_exists_or_invalid(self):
        user, token = self.signin_as_admin()
        payload = self.samples[0]
        payload['password'] = '*'
        res = self.api_request(
            BY_ID_2_URL, 'PATCH', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_are_empty(self):
        user, token = self.signin_as_admin()
        payload = self.samples[0]
        payload['username'] = ''
        payload['password'] = ''
        payload['email'] = None
        res = self.api_request(
            BY_ID_2_URL, 'PATCH', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_valid_delete(self):
        user, token = self.signin_as_admin()
        payload = self.samples[0]
        res = self.api_request(
            BY_ID_2_URL, 'DELETE', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual({}, res.data['user'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_delete_when_not_authenticate_well(self):
        user, token = self.signin_as_admin()
        payload = self.samples[0]
        payload['password'] = 'bla'
        res = self.api_request(
            BY_ID_2_URL, 'DELETE', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors'])
        self.assertEqual(token, res.data['token'])
