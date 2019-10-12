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

CURRENT_URL = reverse('users:current')


class CurrentUserAPITests(PrivateUsersAPITests):
    '''Test current user API.'''

    def test_retrieve(self):
        payload = self.samples[0]
        user, token = self.signin(payload)
        res = self.api_request(CURRENT_URL, 'GET', payload, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user['username'], res.data['user']['username'])
        self.assertEqual(token, res.data['token'])

    def test_valid_update(self):
        payload = self.samples[0]
        user, token = self.signin(payload)
        payload = self.samples[2]
        res = self.api_request(
            CURRENT_URL, 'PATCH', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user['id'], res.data['user']['id'])
        self.assertEqual(payload['username'], res.data['user']['username'])
        self.assertEqual(payload['email'], res.data['user']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_exists_or_invalid(self):
        payload = self.samples[0]
        user, token = self.signin(payload)
        payload = self.samples[1]
        payload['password'] = '*'
        res = self.api_request(
            CURRENT_URL, 'PATCH', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_are_empty(self):
        payload = self.samples[0]
        user, token = self.signin(payload)
        payload['username'] = ''
        payload['password'] = ''
        payload['email'] = None
        res = self.api_request(
            CURRENT_URL, 'PATCH', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_valid_delete(self):
        payload = self.samples[0]
        user, token = self.signin(payload)
        res = self.api_request(
            CURRENT_URL, 'DELETE', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual({}, res.data['user'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_delete_when_not_authenticate_well(self):
        payload = self.samples[0]
        user, token = self.signin(payload)
        payload['password'] = 'blabla'
        res = self.api_request(
            CURRENT_URL, 'DELETE', payload=payload, token=token
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors'])
        self.assertEqual(token, res.data['token'])
