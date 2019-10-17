from django.test import TestCase

from django.contrib.auth import get_user_model

from funds.models import Fund


class FundsTests(TestCase):

    def setUp(self):

        self.samples = {
            'users': [
                {'username': 'user1', 'password': 'pass123', 'email': 'user1@testemail.org'},  # noqa: E501
                {'username': 'user2', 'password': 'pass234', 'email': 'user2@testemail.org'},  # noqa: E501
            ],

            'funds': [
                {'user': None, 'code': '1', 'name': 'CASH'},
                {'user': None, 'code': '2', 'name': 'VISA'},
                {'user': None, 'code': '3', 'name': 'MASTERCARD'},                
                {'user': None, 'code': '1', 'name': 'CASH'},
                {'user': None, 'code': '2', 'name': 'PREPAID CARD'},
            ],
        }

    def create_fund(self, user, fund):
        fund['user'] = user
        
        return Fund.objects.create(**fund)
