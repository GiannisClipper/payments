from django.test import TestCase
from django.test import Client
from rest_framework import status

from apps.constants import WELCOME, SIGNATURE, LINKEDIN_URL, GITHUB_URL


class RootRequestTest(TestCase):

    def test_root_response(self):
        client = Client()
        res = client.get('/')

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertIn(WELCOME.encode(), res.content)
        self.assertIn(SIGNATURE.encode(), res.content)
        self.assertIn(LINKEDIN_URL.encode(), res.content)
        self.assertIn(GITHUB_URL.encode(), res.content)
