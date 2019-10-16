from django.test import TestCase

from django.contrib.auth import get_user_model


class FundsTests(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            **{'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
        )
        self.user2 = get_user_model().objects.create_user(
            **{'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
        )
        self.admin1 = get_user_model().objects.create_superuser(
            **{'username': 'admin1', 'password': 'pass123', 'email': 'admin1@testemail.org'},  # noqa: E501
        )

        self.samples = [
            {'user': self.user1, 'code': '1', 'name': 'CASH'},
            {'user': self.user1, 'code': '2', 'name': 'VISA'},
            {'user': self.user1, 'code': '3', 'name': 'MASTERCARD'},
            {'user': self.user2, 'code': '1', 'name': 'CASH'},
            {'user': self.user2, 'code': '2', 'name': 'PREPAID CARD'},
        ]
