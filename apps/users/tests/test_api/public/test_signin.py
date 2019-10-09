from . import PublicUsersAPITests

from django.urls import reverse

from rest_framework import status

from users.constants import (
    USERNAME_REQUIRED,
    PASSWORD_REQUIRED,
    INPUT_NOT_MATCH,
)

SIGNIN_URL = reverse('users:signin')


class SigninAPITests(PublicUsersAPITests):
    '''Test users signin API requests.'''

    def test_valid_signin(self):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])
        payload = self.samples[1]
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data['user'])
        self.assertIn('token', res.data)

    def test_invalid_signin_when_values_are_empty(self):
        payload = {'username': '', 'password': ''}
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])

    def test_invalid_signin_when_credentials_not_match(self):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])
        payload = {'username': '*', 'password': '*'}
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors']['error'])
