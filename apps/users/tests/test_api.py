from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from unittest import skip  # noqa: F401

from rest_framework.test import APIClient
from rest_framework import status

import json

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
)

SIGNUP_URL = reverse('users:signup')
SIGNIN_URL = reverse('users:signin')


class UsersAPITests(TestCase):

    def create_user(self, **params):
        return get_user_model().objects.create_user(**params)

    def setUp(self):
        self.payloads = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
            {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
        ]

        self.client = APIClient()


class PublicUsersAPITests(UsersAPITests):
    '''Test users API requests that not require authentication'''

    def test_valid_signup(self):
        res = self.client.post(
            SIGNUP_URL,
            json.dumps({'user': self.payloads[0]}),
            content_type="application/json",
        )
        res.data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['user']['id'])
        self.assertTrue(user.check_password(self.payloads[0]['password']))
        self.assertNotIn('password', res.data)

    def test_invalid_signup_with_empty_values(self):
        res = self.client.post(
            SIGNUP_URL,
            json.dumps({'user': {'username': '', 'password': '', 'email': ''}}),
            content_type="application/json",
        )
        res.data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])

    def test_valid_signin(self):
        self.create_user(**self.payloads[0])
        self.create_user(**self.payloads[1])
        res = self.client.post(
            SIGNIN_URL,
            json.dumps({'user': self.payloads[1]}),
            content_type="application/json",
        )
        res.data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data['user'])
        self.assertIn('token', res.data)

    def test_invalid_signin_with_empty_values(self):
        res = self.client.post(
            SIGNIN_URL,
            json.dumps({'user': {'username': '', 'password': ''}}),
            content_type="application/json",
        )
        res.data = json.loads(res.data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])


class PrivateUsersAPITests(UsersAPITests):
    '''Test users API requests that require authentication'''

    pass
