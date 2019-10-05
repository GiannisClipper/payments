from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from unittest import skip  # noqa: F401

from rest_framework.test import APIClient
from rest_framework import status

import json

from apps.settings import JWTOKEN_PREFIX

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,

    INPUT_NOT_MATCH
)

SIGNUP_URL = reverse('users:signup')
SIGNIN_URL = reverse('users:signin')
CURRENT_URL = reverse('users:current')



class UsersAPITests(TestCase):

    def create_user(self, **params):
        return get_user_model().objects.create_user(**params)

    def send_json(self, url, method='GET', payload=None, token=None):
        if token:
            self.client.credentials(
                HTTP_AUTHORIZATION=f'{JWTOKEN_PREFIX} {token}'
            )

        payload = json.dumps(payload)
        content_type = 'application/json'

        if method == 'POST':
            res = self.client.post(url, payload, content_type=content_type)
        else:
            res = self.client.get(url, content_type=content_type)
            print(res.data)

        res.data = json.loads(res.data)
        
        return res

    def setUp(self):
        self.samples = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
            {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
        ]

        self.client = APIClient()


class PublicUsersAPITests(UsersAPITests):
    '''Test users API requests that not require authentication'''

    def test_valid_signup(self):
        payload = {'user': self.samples[0]}
        res = self.send_json(SIGNUP_URL, 'POST', payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['user']['id'])
        self.assertTrue(user.check_password(self.samples[0]['password']))
        self.assertNotIn('password', res.data)

    def test_invalid_signup_when_values_are_empty_or_missing(self):
        payload = {'user': {'username': '', 'password': ''}}
        res = self.send_json(SIGNUP_URL, 'POST', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])
        self.assertIn(EMAIL_REQUIRED, res.data['errors']['email'])

    def test_invalid_signup_when_values_exists_or_invalid(self):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])
        self.samples[0]['password'] = '*'
        payload = {'user': self.samples[0]}
        res = self.send_json(SIGNUP_URL, 'POST', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_EXISTS, res.data['errors']['username'])
        self.assertIn(PASSWORD_TOO_SHORT, res.data['errors']['password'])
        self.assertIn(EMAIL_EXISTS, res.data['errors']['email'])

    def test_valid_signin(self):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])
        payload = {'user': self.samples[1]}
        res = self.send_json(SIGNIN_URL, 'POST', payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data['user'])
        self.assertIn('token', res.data)

    def test_invalid_signin_when_values_are_empty(self):
        payload = {'user': {'username': '', 'password': ''}}
        res = self.send_json(SIGNIN_URL, 'POST', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(USERNAME_REQUIRED, res.data['errors']['username'])
        self.assertIn(PASSWORD_REQUIRED, res.data['errors']['password'])

    def test_invalid_signin_when_credentials_not_match(self):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])
        payload = {'user': {'username': '*', 'password': '*'}}
        res = self.send_json(SIGNIN_URL, 'POST', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertIn(INPUT_NOT_MATCH, res.data['errors']['error'])


class PrivateUsersAPITests(UsersAPITests):
    '''Test users API requests that require authentication'''

    def signin(self, payload):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])
        res = self.send_json(SIGNIN_URL, 'POST', payload)

        return res

    def test_get_current_user(self):
        payload = {'user': self.samples[0]}
        signin_res = self.signin(payload)
        print(signin_res.data)
        token = signin_res.data['token']
        res = self.send_json(CURRENT_URL, 'GET', token=token)

        self.assertIn('bla', signin_res.data)