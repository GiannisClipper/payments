from .. import FundsAPITests

from django.urls import reverse

SIGNIN_URL = reverse('users:signin')


class PrivateFundsAPITests(FundsAPITests):
    '''Test funds API requests that require authentication.'''

    def signin(self, payload):
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)

        return res.data['user'], res.data['token']
