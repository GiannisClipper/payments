from django.test import TestCase

from django.contrib.auth import get_user_model

import copy

USER_SAMPLES = {
    1: {'username': 'user1', 'password': 'pass123', 'password2': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
    2: {'username': 'user2', 'password': 'pass234', 'password2': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
    3: {'username': 'user3', 'password': 'pass345', 'password2': 'pass345', 'email': 'user3@testemail.org'},  # noqa: E501
}

ADMIN_SAMPLES = {
    1: {'username': 'admin1', 'password': 'pass123', 'password2': 'pass123', 'email': 'admin1@testemail.org'},  # noqa: E501
    2: {'username': 'admin2', 'password': 'pass234', 'password2': 'pass234', 'email': 'admin2@testemail.org'},  # noqa: E501
}


class UserCreateMethods:

    def create_admin(self, **sample):
        return get_user_model().objects.create_superuser(**sample)

    def create_admins(self, samples):
        for user in samples.values():
            self.create_admin(**user)

    def create_user(self, **sample):
        return get_user_model().objects.create_user(**sample)

    def create_users(self, samples):
        for user in samples.values():
            self.create_user(**user)


class UsersTests(TestCase, UserCreateMethods):

    def setUp(self):
        self.samples = {
            'admins': copy.deepcopy(ADMIN_SAMPLES),
            'users': copy.deepcopy(USER_SAMPLES)
        }
