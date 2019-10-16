from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from unittest import skip  # noqa: F401

from users.models import User
from users.tests import UsersTests

from users.constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
)


class UserModelTests(UsersTests):
    pass


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

    def test_update(self):
        init_user = User.objects.create_superuser(**self.samples[0])
        user = init_user.update(**self.samples[1])

        self.assertEqual(user.pk, init_user.pk)
        self.assertEqual(user.username, self.samples[1]['username'])
        self.assertTrue(user.check_password(self.samples[1]['password']))
        self.assertEqual(user.email, self.samples[1]['email'])

    def test_delete(self):
        user = User.objects.create_superuser(**self.samples[1])
        user.delete()  # Built-in method

        self.assertEqual(user.pk, None)

    def test_str_representation(self):
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(str(user), self.samples[0]['username'])


class UserModelValidationOnCreateTests(UserModelTests):

    def test_required_errors(self):
        errors = ''
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

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
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

    def test_unique_errors(self):
        errors = ''
        User.objects.create_user(**self.samples[0])

        try:
            User.objects.create_user(**self.samples[0])
        except Exception as err:
            errors = str(err)

        self.assertIn(USERNAME_EXISTS, errors)
        self.assertIn(EMAIL_EXISTS, errors)

    def test_password_min_length(self):
        self.samples[0]['password'] = '*'

        try:
            User.objects.create_user(**self.samples[0])
        except Exception as err:
            errors = str(err)

        self.assertIn(PASSWORD_TOO_SHORT, errors)

    def test_email_normalization(self):
        self.samples[0]['email'] = self.samples[0]['email'].upper()
        user = User.objects.create_user(**self.samples[0])

        self.assertEqual(
            user.email,
            self.samples[0]['email'].split('@')[0] + '@' +
            self.samples[0]['email'].split('@')[1].lower()
        )


class UserModelValidationOnUpdateTests(UserModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        user = User.objects.create_user(**self.samples[0])
        self.samples[0]['username'] = '        '
        self.samples[0]['password'] = '        '
        self.samples[0]['email'] = None

        try:
            user.update(**self.samples[0])
        except ValidationError as err:
            errors = str(err)

        self.assertIn(USERNAME_REQUIRED, errors)
        self.assertIn(PASSWORD_REQUIRED, errors)
        self.assertIn(EMAIL_REQUIRED, errors)

    def test_unique_errors(self):
        errors = ''
        User.objects.create_user(**self.samples[0])
        user = User.objects.create_user(**self.samples[1])

        try:
            user.update(**self.samples[0])
        except Exception as err:
            errors = str(err)

        self.assertIn(USERNAME_EXISTS, errors)
        self.assertIn(EMAIL_EXISTS, errors)
