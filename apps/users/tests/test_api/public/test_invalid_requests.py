from django.urls import reverse
from rest_framework import status

from . import PublicUsersAPITests

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
    INPUT_NOT_MATCH,
)

SIGNUP_URL = reverse('users:signup')
SIGNIN_URL = reverse('users:signin')


class SignupAPITests(PublicUsersAPITests):
    '''Test users signup API requests.'''

    def test_signup_when_values_are_empty_or_missing(self):
        sample = {'username': '', 'password': ''}
        res = self.api_request(SIGNUP_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])

    def test_signup_when_values_exists_or_invalid(self):
        self.create_users(self.samples['users'])
        sample = self.samples['users'][1]
        sample['password'] = '*'
        res = self.api_request(SIGNUP_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])


class SigninAPITests(PublicUsersAPITests):
    '''Test users signin API requests.'''

    def test_signin_when_values_are_empty(self):
        sample = {'username': '', 'password': ''}
        res = self.api_request(SIGNIN_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])

    def test_signin_when_credentials_not_match(self):
        self.create_users(self.samples['users'])
        sample = {'username': 'blabla', 'password': 'blabla'}
        res = self.api_request(SIGNIN_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors']['error'])
