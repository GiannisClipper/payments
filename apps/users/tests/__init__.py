from django.test import TestCase

import copy

SAMPLES = [
    {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},
    {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},
    {'username': 'user3', 'password': 'pass345', 'email': 'user3@testemail.org'},
    {'username': 'user4', 'password': 'pass456', 'email': 'user4@testemail.org'},
    {'username': 'user5', 'password': 'pass567', 'email': 'user5@testemail.org'},
]


class UsersTests(TestCase):

    def setUp(self):

        self.samples = copy.deepcopy(SAMPLES)
