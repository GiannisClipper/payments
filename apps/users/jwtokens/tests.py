from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest import skip  # noqa: F401

from datetime import datetime

from apps.settings import JWTOKEN_DURATION


class JWTokenTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user1',
            password='pass123',
            password2='pass123',
            email='user1@testemail.org'
        )

    def test_encode_token_key(self):
        key = self.user.token

        # JWTokens are consisted of 3 parts seperated with dots
        self.assertEqual(len(key.split('.')), 3)

    def test_decode_token_key(self):
        key = self.user.token
        key = key.encode('utf-8')  # Convert str to binary
        result = get_user_model().decode_token_key(key)

        self.assertEqual(result['user_id'], self.user.pk)
        now = datetime.timestamp(datetime.utcnow())
        expiration = now + JWTOKEN_DURATION
        self.assertTrue(expiration - result['expiration'] <= 1)

    def test_decode_when_token_key_is_invalid(self):
        key = self.user.token
        key = (key + 'invalid').encode('utf-8')  # Convert str to binary

        with self.assertRaises(Exception):
            get_user_model().decode_key(key)

    def test_check_when_token_key_is_expired(self):
        with self.assertRaises(Exception):
            get_user_model().check_if_key_is_expired(1)

    def test_check_when_user_in_token_not_exists(self):
        with self.assertRaises(Exception):
            get_user_model().check_if_user_in_key_exists(1)

    def test_check_when_user_in_token_is_not_active(self):
        self.user.is_active = False
        with self.assertRaises(Exception):
            get_user_model().check_if_user_in_key_is_active(self.user)

    def test_compose_token_header(self):
        key = self.user.token
        header = get_user_model().compose_token_header(key)

        # JWToken headers are consisted of 2 parts seperated with space
        self.assertEqual(len(header.split(' ')), 2)

    def test_decompose_token_header(self):
        key = self.user.token
        header = get_user_model().compose_token_header(key)
        header = header.encode('utf-8')  # Convert str to binary
        returned_key = get_user_model().decompose_token_header(header)

        self.assertEqual(returned_key, key)

    def test_decompose_when_token_header_is_invalid(self):
        header = 'Anything_but_not_a_valid_header'
        header = header.encode('utf-8')  # Convert str to binary

        with self.assertRaises(Exception):
            get_user_model().decompose_token_header(header)

    def test_decompose_when_token_prefix_is_invalid(self):
        key = self.user.token
        header = get_user_model().compose_token_header(key)
        header = ('invalid' + header).encode('utf-8')  # Convert str to binary

        with self.assertRaises(Exception):
            get_user_model().decompose_token_header(header)
