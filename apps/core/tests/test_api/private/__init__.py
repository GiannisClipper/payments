from django.urls import reverse

from django.contrib.auth import get_user_model

from core.tests.test_api import APITests

SIGNIN_URL = reverse('users:signin')


class PrivateAPITests(APITests):
    '''Test API requests that require authentication.'''

    def _signin(self, payload):
        namespace, self.namespace = self.namespace, 'user'
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)
        self.namespace = namespace

        return res.data['user'], res.data['token']

    def signin_as_user(self, payload):
        for user in self.samples['users']:
            self.create_user(**user)

        return self._signin(payload)

    def signin_as_admin(self, payload):
        for user in self.samples['users']:
            self.create_admin(**user)

        return self._signin(payload)


class OwnerPrivateAPITests(PrivateAPITests):
    def setUp(self):
        super().setUp()
        sample = self.samples['users'][0]
        user_, self.token = self.signin_as_user(sample)
        self.user = get_user_model().objects.get(pk=user_['id'])
        self.user2 = get_user_model().objects.get(pk=2)


class AdminPrivateAPITests(PrivateAPITests):
    def setUp(self):
        super().setUp()
        sample = self.samples['users'][0]
        user_, self.token = self.signin_as_admin(sample)
        self.user = get_user_model().objects.get(pk=user_['id'])
        self.user2 = get_user_model().objects.get(pk=2)
