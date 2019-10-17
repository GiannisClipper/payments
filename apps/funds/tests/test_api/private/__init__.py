from .. import FundsAPITests

from django.urls import reverse

SIGNIN_URL = reverse('users:signin')


class PrivateFundsAPITests(FundsAPITests):
    '''Test funds API requests that require authentication.'''

    def _signin(self, payload):
        self.namespace = 'user'
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)
        self.namespace = 'fund'

        return res.data['user'], res.data['token']

    def signin(self, payload):
        for user in self.samples['users']:
            self.create_user(**user)

        return self._signin(payload)

    def signin_as_admin(self, payload):
        for user in self.samples['users']:
            self.create_admin(**user)

        return self._signin(payload)
