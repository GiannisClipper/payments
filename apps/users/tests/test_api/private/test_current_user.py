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

    URL = CURRENT_URL

    def test_retrieve(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        res = self.api_request(self.URL, 'GET', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user['username'], res.data['user']['username'])
        self.assertEqual(token, res.data['token'])

    def test_valid_update(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        sample['username'] += 'blabla'
        sample['email'] += 'blabla'
        res = self.api_request(self.URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user['id'], res.data['user']['id'])
        self.assertEqual(sample['username'], res.data['user']['username'])
        self.assertEqual(sample['email'], res.data['user']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_exists_or_invalid(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        sample = self.samples['users'][1]
        sample['password'] = '*'
        res = self.api_request(self.URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_update_when_values_are_empty(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        sample['username'] = ''
        sample['password'] = ''
        sample['email'] = None
        res = self.api_request(self.URL, 'PATCH', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])
        self.assertEqual(token, res.data['token'])

    def test_valid_delete(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        res = self.api_request(self.URL, 'DELETE', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual({}, res.data['user'])
        self.assertEqual(token, res.data['token'])

    def test_invalid_delete_when_not_authenticate_well(self):
        sample = self.samples['users'][0]
        user, token = self.signin_as_user(sample)
        sample['password'] = 'blabla'
        res = self.api_request(self.URL, 'DELETE', payload=sample, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors'])
        self.assertEqual(token, res.data['token'])
