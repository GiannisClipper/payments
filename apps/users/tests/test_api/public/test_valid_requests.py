from django.urls import reverse
from rest_framework import status

from django.contrib.auth import get_user_model

from . import PublicUsersAPITests

SIGNUP_URL = reverse('users:signup')
SIGNIN_URL = reverse('users:signin')


class SignupAPITests(PublicUsersAPITests):
    '''Test users signup API requests.'''

    def test_valid_signup(self):
        sample = self.samples['users'][1]
        res = self.api_request(SIGNUP_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['user']['id'])
        self.assertTrue(user.check_password(sample['password']))
        self.assertNotIn('password', res.data)


class SigninAPITests(PublicUsersAPITests):
    '''Test users signin API requests.'''

    def test_valid_signin(self):
        self.create_users(self.samples['users'])
        sample = self.samples['users'][1]
        res = self.api_request(SIGNIN_URL, 'POST', payload=sample)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', res.data['user'])
        self.assertIn('token', res.data)
