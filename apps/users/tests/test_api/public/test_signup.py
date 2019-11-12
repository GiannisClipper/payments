from . import PublicUsersAPITests

from django.urls import reverse

from django.contrib.auth import get_user_model

from rest_framework import status

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
)

SIGNUP_URL = reverse('users:signup')


class SignupAPITests(PublicUsersAPITests):
    '''Test users signup API requests.'''

    def test_valid_signup(self):
        sample = self.samples['users'][1]
        res = self.api_request(SIGNUP_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['user']['id'])
        self.assertTrue(user.check_password(sample['password']))
        self.assertNotIn('password', res.data)

    def test_invalid_signup_when_values_are_empty_or_missing(self):
        sample = {'username': '', 'password': ''}
        res = self.api_request(SIGNUP_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])

    def test_invalid_signup_when_values_exists_or_invalid(self):
        self.create_users(self.samples['users'])
        sample = self.samples['users'][1]
        sample['password'] = '*'
        res = self.api_request(SIGNUP_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])
