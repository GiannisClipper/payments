from django.urls import reverse

from django.contrib.auth import get_user_model

from core.tests.test_api import APITests

from users.tests import UserCreateMethods

SIGNIN_URL = reverse('users:signin')


class PrivateAPITests(APITests):
    '''Test API requests that require authentication.'''

    def signin(self, payload):
        namespace, self.namespace = self.namespace, 'user'
        res = self.api_request(SIGNIN_URL, 'POST', payload=payload)
        self.namespace = namespace

        return res.data['user'], res.data['token']


class OwnerPrivateAPITests(PrivateAPITests, UserCreateMethods):
    def setUp(self):
        super().setUp()

        self.create_users(self.samples['users'])
        sample = self.samples['users'][1]
        user_, self.token = self.signin(sample)

        self.user = get_user_model().objects.get(pk=user_['id'])
        self.user2 = get_user_model().objects.get(pk=2)


class AdminPrivateAPITests(PrivateAPITests, UserCreateMethods):
    def setUp(self):
        super().setUp()

        self.create_admins(self.samples['users'])
        sample = self.samples['users'][1]
        user_, self.token = self.signin(sample)

        self.user = get_user_model().objects.get(pk=user_['id'])
        self.user2 = get_user_model().objects.get(pk=2)
