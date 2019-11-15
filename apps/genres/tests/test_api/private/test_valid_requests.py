from unittest import skip  # noqa: F401
from rest_framework import status

from genres.tests.test_api import ROOT_URL, BY_ID_1_URL, LIST_URL

from . import AdminPrivateGenresAPITests, OwnerPrivateGenresAPITests


class AdminRequests(AdminPrivateGenresAPITests):
    '''Test owner's valid requests to genres API.'''

    # Signed admin has id > 1 other than owner's id in samples (funds, genres)

    def test_post(self):
        sample = self.samples['genres'][11]
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre']['user']['id'], sample['user']['id'])
        self.assertEqual(res.data['genre']['code'], sample['code'])
        self.assertEqual(res.data['genre']['name'], sample['name'])
        self.assertEqual(res.data['genre']['is_income'], sample['is_income'])
        self.assertEqual(res.data['genre']['fund']['id'], sample['fund']['id'])
        self.assertIn(f"/genres/{res.data['genre']['id']}/", res.data['genre']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_get(self):
        sample = self.samples['genres'][11]
        self.create_genre(**sample)

        res = self.api_request(BY_ID_1_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre']['user']['id'], sample['user']['id'])
        self.assertEqual(res.data['genre']['code'], sample['code'])
        self.assertEqual(res.data['genre']['name'], sample['name'])
        self.assertEqual(res.data['genre']['is_income'], sample['is_income'])
        self.assertEqual(res.data['genre']['fund']['id'], sample['fund']['id'])
        self.assertIn(f"/genres/{res.data['genre']['id']}/", res.data['genre']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_patch(self):
        sample = self.samples['genres'][11]
        self.create_genre(**sample)
        sample = self.samples['genres'][12]

        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre']['code'], sample['code'])
        self.assertEqual(res.data['genre']['name'], sample['name'])
        self.assertEqual(res.data['genre']['is_income'], sample['is_income'])
        self.assertEqual(res.data['genre']['fund']['id'], sample['fund']['id'])
        self.assertEqual(res.data['token'], self.token)

    def test_delete(self):
        sample = self.samples['genres'][11]
        self.create_genre(**sample)

        res = self.api_request(BY_ID_1_URL, 'DELETE', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre'], {})
        self.assertEqual(res.data['token'], self.token)


class OwnerRequest(OwnerPrivateGenresAPITests, AdminRequests):
    '''Test owner's valid requests to genres API.'''

    # Signed user has id = 1 same with owner's id in samples (funds, genres)


class AdminGetList(AdminPrivateGenresAPITests):
    '''Test admin's list requests to funds API.'''

    def setUp(self):
        super().setUp()
        self.create_genres(self.samples['genres'])

    def test_get_list(self):
        res = self.api_request(LIST_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genres', res.data)
        self.assertEqual(len(res.data['genres']), len(self.samples['genres']))
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_other_user_id(self):
        res = self.api_request(LIST_URL + '?user_id=1', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genres', res.data)
        self.assertEqual(res.data['token'], self.token)


class OwnerGetList(OwnerPrivateGenresAPITests):
    '''Test owner's list requests to funds API.'''

    def setUp(self):
        super().setUp()
        self.create_genres(self.samples['genres'])

    def test_get_list(self):
        res = self.api_request(LIST_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genres', res.data)
        self.assertNotEqual(len(res.data['genres']), len(self.samples['genres']))
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_self_user_id(self):
        res = self.api_request(LIST_URL + '?user_id=1', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genres', res.data)
        self.assertEqual(res.data['token'], self.token)
