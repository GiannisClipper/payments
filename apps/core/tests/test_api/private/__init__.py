from django.urls import reverse

from core.tests.test_api import APITests

SIGNIN_URL = reverse('users:signin')


class PrivateAPITests(APITests):
    '''Test API requests that require authentication.'''

    def signin(self, payload):
        namespace, self.namespace = self.namespace, 'user'
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)
        self.namespace = namespace

        return res.data['user'], res.data['token']
