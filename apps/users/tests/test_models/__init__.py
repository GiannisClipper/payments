from unittest import skip  # noqa: F401

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
        sample = self.samples['users'][0]
        user = self.create_user(**sample)

        self.assertEqual(user.username, sample['username'])
        self.assertTrue(user.check_password(sample['password']))
        self.assertEqual(user.email, sample['email'])
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        sample = self.samples['users'][0]
        user = self.create_admin(**sample)

        self.assertEqual(user.username, sample['username'])
        self.assertTrue(user.check_password(sample['password']))
        self.assertEqual(user.email, sample['email'])
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_update(self):
        sample = self.samples['users'][0]
        init_user = self.create_admin(**sample)
        sample = self.samples['users'][1]
        user = init_user.update(**sample)

        self.assertEqual(user.pk, init_user.pk)
        self.assertEqual(user.username, sample['username'])
        self.assertTrue(user.check_password(sample['password']))
        self.assertEqual(user.email, sample['email'])

    def test_delete(self):
        sample = self.samples['users'][1]
        user = self.create_admin(**sample)
        user.delete()  # Built-in method

        self.assertEqual(user.pk, None)

    def test_str_representation(self):
        sample = self.samples['users'][0]
        user = self.create_user(**sample)

        self.assertEqual(str(user), sample['username'])


class UserModelValidationOnCreateTests(UserModelTests):

    def test_required_errors(self):
        errors = ''
        sample = self.samples['users'][0]
        del sample['username']
        del sample['password']
        del sample['email']

        try:
            self.create_user(**sample)
        except ValidationError as err:
            errors = str(err)

        self.assertIn(USERNAME_REQUIRED, errors)
        self.assertIn(PASSWORD_REQUIRED, errors)
        self.assertIn(EMAIL_REQUIRED, errors)

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        sample = self.samples['users'][0]
        sample['username'] = '        '
        sample['password'] = '        '
        sample['email'] = None

        try:
            self.create_user(**sample)
        except ValidationError as err:
            errors = str(err)

        self.assertIn(USERNAME_REQUIRED, errors)
        self.assertIn(PASSWORD_REQUIRED, errors)
        self.assertIn(EMAIL_REQUIRED, errors)

    def test_unique_errors(self):
        errors = ''
        sample = self.samples['users'][0]
        self.create_user(**sample)

        try:
            self.create_user(**sample)
        except Exception as err:
            errors = str(err)

        self.assertIn(USERNAME_EXISTS, errors)
        self.assertIn(EMAIL_EXISTS, errors)

    def test_password_min_length(self):
        sample = self.samples['users'][0]
        sample['password'] = '*'

        try:
            self.create_user(**sample)
        except Exception as err:
            errors = str(err)

        self.assertIn(PASSWORD_TOO_SHORT, errors)

    def test_email_normalization(self):
        sample = self.samples['users'][0]
        sample['email'] = sample['email'].upper()
        user = self.create_user(**sample)

        self.assertEqual(
            user.email,
            sample['email'].split('@')[0] + '@' +
            sample['email'].split('@')[1].lower()
        )


class UserModelValidationOnUpdateTests(UserModelTests):

    def test_required_errors_by_passing_empty_values(self):
        errors = ''
        sample = self.samples['users'][0]
        user = self.create_user(**sample)
        sample['username'] = '        '
        sample['password'] = '        '
        sample['email'] = None

        try:
            user.update(**sample)
        except ValidationError as err:
            errors = str(err)

        self.assertIn(USERNAME_REQUIRED, errors)
        self.assertIn(PASSWORD_REQUIRED, errors)
        self.assertIn(EMAIL_REQUIRED, errors)

    def test_unique_errors(self):
        errors = ''
        sample1 = self.samples['users'][0]
        self.create_user(**sample1)
        sample2 = self.samples['users'][1]
        user = self.create_user(**sample2)

        try:
            user.update(**sample1)
        except Exception as err:
            errors = str(err)

        self.assertIn(USERNAME_EXISTS, errors)
        self.assertIn(EMAIL_EXISTS, errors)
