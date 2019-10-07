from django.test import TestCase
from unittest import skip  # noqa: F401
from django.contrib.auth import get_user_model
from datetime import datetime

from .handlers import JWTokenHandler

from apps.settings import JWTOKEN_DURATION


class JWTokenTests(TestCase):

    def encode_key(self):
        user = get_user_model().objects.create_user(**self.samples[0])
        now = datetime.timestamp(datetime.utcnow())
        expiration = now + JWTOKEN_DURATION
        payload = {'id': user.pk, 'expiration': expiration}
        key = JWTokenHandler.encode_key(payload)

        return payload, key

    def setUp(self):
        self.samples = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
            {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
        ]

    def test_encode_key(self):
        payload, key = self.encode_key()

        # JWTokens are consisted of 3 parts seperated with dots
        self.assertEqual(len(key.split('.')), 3)

    def test_decode_key(self):
        payload, key = self.encode_key()
        key = key.encode('utf-8')  # Convert str to binary
        returned_payload = JWTokenHandler.decode_key(key)

        self.assertEqual(returned_payload, payload)

    def test_decode_when_key_invalid(self):
        payload, key = self.encode_key()
        key = (key + 'invalid').encode('utf-8')  # Convert str to binary

        with self.assertRaises(Exception):
            JWTokenHandler.decode_key(key)

    def test_check_when_key_is_expired(self):
        with self.assertRaises(Exception):
            JWTokenHandler.check_if_key_is_expired(1)

    def test_check_when_user_in_key_not_exists(self):
        with self.assertRaises(Exception):
            JWTokenHandler.check_if_user_in_key_exists(1)

    def test_check_when_user_in_key_is_not_active(self):
        user = get_user_model().objects.create_user(**self.samples[0])
        user.is_active = False
        with self.assertRaises(Exception):
            JWTokenHandler.check_if_user_in_key_is_active(user)

    def test_compose_header(self):
        payload, key = self.encode_key()
        header = JWTokenHandler.compose_header(key)

        # JWToken headers are consisted of 2 parts seperated with space
        self.assertEqual(len(header.split(' ')), 2)

    def test_decompose_header(self):
        payload, key = self.encode_key()
        header = JWTokenHandler.compose_header(key)
        header = header.encode('utf-8')  # Convert str to binary
        returned_key = JWTokenHandler.decompose_header(header)

        self.assertEqual(returned_key, key)

    def test_decompose_when_header_invalid(self):
        header = 'Anything_but_not_a_valid_header'
        header = header.encode('utf-8')  # Convert str to binary

        with self.assertRaises(Exception):
            JWTokenHandler.decompose_header(header)

    def test_decompose_when_prefix_invalid(self):
        payload, key = self.encode_key()
        header = JWTokenHandler.compose_header(key)
        header = ('invalid' + header).encode('utf-8')  # Convert str to binary

        with self.assertRaises(Exception):
            JWTokenHandler.decompose_header(header)
