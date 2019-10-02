from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from unittest import skip  # noqa: F401

from datetime import datetime

from users.models import User
from users.models import JWTokenHandler

from apps.settings import JWTOKEN_DURATION

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
)


class UserModelTests(TestCase):

    def setUp(self):
        self.samples = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
            {'username': 'user2', 'password': 'pass123', 'email': 'user2@testemail.org'},  # noqa: E501
        ]


class UserModelBasicTests(UserModelTests):

    def test_model_as_auth_model(self):
        self.assertEqual(get_user_model(), User)

    def test_model_structure(self):
        fields = [x.name for x in User._meta.get_fields()]

        self.assertTrue('username' in fields)
        self.assertTrue('password' in fields)
        self.assertTrue('email' in fields)
        self.assertTrue('is_staff' in fields)
        self.assertTrue('is_superuser' in fields)
        self.assertTrue('is_active' in fields)
        self.assertTrue('created_at' in fields)
        self.assertTrue('updated_at' in fields)

    def test_create_user(self):
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(user.username, self.samples[0]['username'])
        self.assertTrue(user.check_password(self.samples[0]['password']))
        self.assertEqual(user.email, self.samples[0]['email'])
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser(**self.samples[0])

        self.assertEqual(user.username, self.samples[0]['username'])
        self.assertTrue(user.check_password(self.samples[0]['password']))
        self.assertEqual(user.email, self.samples[0]['email'])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_str_representation(self):
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(self.samples[0]['username'], str(user))


class UserModelValidationTests(UserModelTests):

    def test_required_fields_errors(self):
        errors = None
        del self.samples[0]['username']
        del self.samples[0]['password']
        del self.samples[0]['email']

        try:
            User.objects.create_user(**self.samples[0])
        except ValidationError as err:
            errors = str(err)

        self.assertIn(USERNAME_REQUIRED, errors)
        self.assertIn(PASSWORD_REQUIRED, errors)
        self.assertIn(EMAIL_REQUIRED, errors)

    def test_required_fields_errors_passing_values(self):
        errors = None
        self.samples[0]['username'] = '        '
        self.samples[0]['password'] = '        '
        self.samples[0]['email'] = None

        try:
            User.objects.create_user(**self.samples[0])
        except ValidationError as err:
            errors = str(err)

        self.assertIn(USERNAME_REQUIRED, errors)
        self.assertIn(PASSWORD_REQUIRED, errors)
        self.assertIn(EMAIL_REQUIRED, errors)

    def test_unique_fields_errors(self):
        errors = None
        User.objects.create_user(**self.samples[0])

        try:
            User.objects.create_user(**self.samples[0])
        except Exception as err:
            errors = str(err)

        self.assertIn(USERNAME_EXISTS, errors)
        self.assertIn(EMAIL_EXISTS, errors)

    def test_email_normalization(self):
        self.samples[0]['email'] = self.samples[0]['email'].upper()
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(
            user.email,
            self.samples[0]['email'].split('@')[0] + '@' +
            self.samples[0]['email'].split('@')[1].lower()
        )


class JWTokenTests(UserModelTests):

    def encode_key(self):
        user = User.objects.create_user(**self.samples[0])
        now = datetime.timestamp(datetime.utcnow())
        expiration = now + JWTOKEN_DURATION
        payload = {'id': user.pk, 'expiration': expiration}
        key = JWTokenHandler.encode_key(payload)

        return payload, key

    def test_encode_key(self):
        payload, key = self.encode_key()

        # JWTokens are consisted of 3 parts seperated with dots
        self.assertEqual(len(key.split('.')), 3)

    def test_decode_key(self):
        payload, key = self.encode_key()
        returned_payload = JWTokenHandler.decode_key(key)

        self.assertEqual(returned_payload, payload)

    def test_decode_when_key_invalid(self):
        payload, key = self.encode_key()
        key += 'go_invalid'

        with self.assertRaises(Exception):
            JWTokenHandler.decode_key(key)

    def test_check_key_when_user_not_exists(self):
        with self.assertRaises(Exception):
            JWTokenHandler.check_key_if_user_exists(1)

    def test_check_key_when_user_not_active(self):
        user = User.objects.create_user(**self.samples[0])
        user.is_active = False
        with self.assertRaises(Exception):
            JWTokenHandler.check_key_if_user_is_active(user)

    def test_check_key_when_expired(self):
        with self.assertRaises(Exception):
            JWTokenHandler.check_key_expiration(1)

    def test_compose_header(self):
        payload, key = self.encode_key()
        header = JWTokenHandler.compose_header(key)

        # JWToken headers are consisted of 2 parts seperated with space
        self.assertEqual(len(header.split(' ')), 2)

    def test_decompose_header(self):
        payload, key = self.encode_key()
        header = JWTokenHandler.compose_header(key)
        returned_key = JWTokenHandler.decompose_header(header)

        self.assertEqual(returned_key, key)

    def test_decompose_when_header_invalid(self):
        header = 'Anything_but_not_a_valid_header'

        with self.assertRaises(Exception):
            JWTokenHandler.decompose_header(header)

    def test_decompose_when_prefix_invalid(self):
        payload, key = self.encode_key()
        header = JWTokenHandler.compose_header(key)
        header = 'go_invalid' + header

        with self.assertRaises(Exception):
            JWTokenHandler.decompose_header(header)
