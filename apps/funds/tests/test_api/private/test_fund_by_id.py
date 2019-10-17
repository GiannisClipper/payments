from . import PrivateFundsAPITests

from django.urls import reverse

from rest_framework import status

from funds.constants import (
    USER_REQUIRED,
    CODE_REQUIRED,
    NAME_REQUIRED,
)

ROOT_URL = reverse('funds:root')
BY_ID_1_URL = reverse('funds:by-id', kwargs={'id': 1})
BY_ID_2_URL = reverse('funds:by-id', kwargs={'id': 2})
BY_ID_3_URL = reverse('funds:by-id', kwargs={'id': 3})



class OwnerAccessCreateFundAPITests(PrivateFundsAPITests):
    '''Test create fund API by owner.'''

    def test_valid_create(self):
        payload = self.samples['users'][0]
        user, token = self.signin(payload)

        payload = self.samples['funds'][0]
        res = self.api_request(ROOT_URL, 'POST', payload=payload, token=token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user['username'], res.data['fund']['user']['username'])
        self.assertEqual(payload['code'], res.data['fund']['code'])
        self.assertEqual(payload['name'], res.data['fund']['name'])
        self.assertIn(
            f"/funds/{res.data['fund']['id']}/", res.data['fund']['url']
        )
        self.assertEqual(token, res.data['token'])

    def test_invalid_create_when_values_exists(self):
        payload = self.samples['users'][0]
        user, token = self.signin(payload)

        payload = self.samples['funds'][0]
        self.api_request(ROOT_URL, 'POST', payload=payload, token=token)
        res = self.api_request(ROOT_URL, 'POST', payload=payload, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])

    def test_invalid_create_when_values_are_empty(self):
        payload = self.samples['users'][0]
        user, token = self.signin(payload)

        payload = {}
        res = self.api_request(ROOT_URL, 'POST', payload=payload, token=token)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', res.data)
        self.assertEqual(token, res.data['token'])


class OwnerAccessFundByIdAPITests(PrivateFundsAPITests):
    '''Test fund-by-id API by owner.'''
  
    def test_valid_retrieve(self):
        payload = self.samples['users'][0]
        user, token = self.signin(payload)

        payload = self.samples['funds'][0]
        res1 = self.api_request(ROOT_URL, 'POST', payload=payload, token=token)
        payload = self.samples['funds'][1]
        res2 = self.api_request(ROOT_URL, 'POST', payload=payload, token=token)
        res3 = self.api_request(BY_ID_1_URL, 'GET', token=token)

        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res3.data, res2.data)
        self.assertEqual(res3.data, res1.data)
