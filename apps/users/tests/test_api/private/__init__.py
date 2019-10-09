from .. import UsersAPITests

from django.urls import reverse

SIGNIN_URL = reverse('users:signin')


class PrivateUsersAPITests(UsersAPITests):
    '''Test users API requests that require authentication.'''

    def signin(self, payload=None):
        self.create_user(**self.samples[0])
        self.create_user(**self.samples[1])

        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)

        return res.data['user'], res.data['token']

    def signin_as_admin(self, payload=None):
        self.create_admin(**self.samples[0])
        self.create_admin(**self.samples[1])

        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)

        return res.data['user'], res.data['token']

    def setUp(self):
        super().setUp()
