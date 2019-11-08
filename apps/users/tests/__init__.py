from django.test import TestCase

from django.contrib.auth import get_user_model

import copy

USER_SAMPLES = [
    {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},
    {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},
    {'username': 'user3', 'password': 'pass345', 'email': 'user3@testemail.org'},
    {'username': 'user4', 'password': 'pass456', 'email': 'user4@testemail.org'},
    {'username': 'user5', 'password': 'pass567', 'email': 'user5@testemail.org'},
]


class UserCreateMethods:

    def create_user(self, **sample):
        return get_user_model().objects.create_user(**sample)

    def create_admin(self, **sample):
        return get_user_model().objects.create_superuser(**sample)


class UsersTests(TestCase, UserCreateMethods):

    def setUp(self):
        self.samples = {
            'users': copy.deepcopy(USER_SAMPLES)
        }
