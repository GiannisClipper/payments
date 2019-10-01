from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest import skip  # noqa: F401

from users.models import User
from users.constants import Msg


class UserModelTests(TestCase):

    def setUp(self):
        self.samples = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
            {'username': 'user2', 'password': 'pass123', 'email': 'user2@testemail.org'},  # noqa: E501
        ]

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

    def test_username_required_error(self):
        error_message, self.samples[0]['username'] = None, None
        try:
            User.objects.create_user(**self.samples[0])
        except Exception as error:
            error_message = str(error)

        self.assertEqual(error_message, Msg.USERNAME_REQUIRED)

    def test_email_required_error(self):
        error_message, self.samples[0]['email'] = None, None
        try:
            User.objects.create_user(**self.samples[0])
        except Exception as error:
            error_message = str(error)

        self.assertEqual(error_message, Msg.EMAIL_REQUIRED)

    def test_email_normalization(self):
        self.samples[0]['email'] = self.samples[0]['email'].upper()
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(
            user.email,
            self.samples[0]['email'].split('@')[0] + '@' +
            self.samples[0]['email'].split('@')[1].lower()
        )

    def test_username_exists_error(self):
        User.objects.create_user(**self.samples[0])
        error_message = None
        self.samples[1]['username'] = self.samples[0]['username']
        try:
            User.objects.create_user(**self.samples[1])
        except Exception as error:
            error_message = str(error)

        self.assertEqual(error_message, Msg.USERNAME_EXISTS)

    def test_email_exists_error(self):
        User.objects.create_user(**self.samples[0])
        error_message = None
        self.samples[1]['email'] = self.samples[0]['email']
        try:
            User.objects.create_user(**self.samples[1])
        except Exception as error:
            error_message = str(error)

        self.assertEqual(error_message, Msg.EMAIL_EXISTS)

    def test_username_str_representation(self):
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(self.samples[0]['username'], str(user))
