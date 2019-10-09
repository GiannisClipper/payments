from . import PrivateUsersAPITests

from django.urls import reverse

from rest_framework import status

LIST_URL = reverse('users:list')


class AllUsersListAPITests(PrivateUsersAPITests):
    '''Test all users list API.'''

    def setUp(self):
        super().setUp()

        # self.create_user(**self.samples[0]) takes over through `signin()`
        # self.create_user(**self.samples[1]) takes over through `signin()`
        self.create_user(**self.samples[2])
        self.create_user(**self.samples[3])
        self.create_admin(**self.samples[4])

    def test_retrieve(self):
        user, token = self.signin_as_admin()
        res = self.api_request(LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('users', res.data)
        self.assertTrue(type(res.data['users']) == list)
        self.assertEqual(token, res.data['token'])

    def test_invalid_retrieve_without_permission(self):
        user, token = self.signin()
        res = self.api_request(LIST_URL, 'GET', token=token)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])
