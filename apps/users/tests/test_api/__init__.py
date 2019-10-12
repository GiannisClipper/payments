from django.contrib.auth import get_user_model

from core.tests import APITests


class UsersAPITests(APITests):

    namespace = 'user'

    def setUp(self):
        super().setUp()

        self.samples = [
            {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
            {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
            {'username': 'user3', 'password': 'pass345', 'email': 'user3@testemail.org'},  # noqa: E501
            {'username': 'user4', 'password': 'pass456', 'email': 'user4@testemail.org'},  # noqa: E501
            {'username': 'user5', 'password': 'pass567', 'email': 'user5@testemail.org'},  # noqa: E501
        ]

    def create_user(self, **sample):
        return get_user_model().objects.create_user(**sample)

    def create_admin(self, **sample):
        return get_user_model().objects.create_superuser(**sample)
