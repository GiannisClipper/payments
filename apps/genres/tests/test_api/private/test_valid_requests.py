from rest_framework import status

from genres.tests.test_api import ROOT_URL, BY_ID_1_URL  #  , LIST_URL

from . import OwnerPrivateGenresAPITests, AdminPrivateGenresAPITests #  , ListAPITests


class OwnerRequest(OwnerPrivateGenresAPITests):
    '''Test owner's valid requests to genres API.'''

    def test_post(self):
        sample = self.samples['genres'][0][0]
        sample['fund'] = self.fund.pk
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre']['user']['username'], self.user.username)
        self.assertEqual(res.data['genre']['code'], sample['code'])
        self.assertEqual(res.data['genre']['name'], sample['name'])
        self.assertEqual(res.data['genre']['is_income'], sample['is_income'])
        self.assertEqual(res.data['genre']['fund']['name'], self.fund.name)
        self.assertIn(f"/genres/{res.data['genre']['id']}/", res.data['genre']['url'])
        self.assertEqual(res.data['token'], self.token)


    def test_get(self):
        sample = self.samples['genres'][0][0]
        self.create_genre(self.user, sample, self.fund)
        res = self.api_request(BY_ID_1_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre']['user']['username'], self.user.username)
        self.assertEqual(res.data['genre']['code'], sample['code'])
        self.assertEqual(res.data['genre']['name'], sample['name'])
        self.assertEqual(res.data['genre']['is_income'], sample['is_income'])
        self.assertEqual(res.data['genre']['fund']['name'], self.fund.name)
        self.assertIn(f"/genres/{res.data['genre']['id']}/", res.data['genre']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_patch(self):
        sample = self.samples['genres'][0][0]
        self.create_genre(self.user, sample, self.fund)
        sample = self.samples['genres'][0][1]
        sample['fund'] = None
        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre']['code'], sample['code'])
        self.assertEqual(res.data['genre']['name'], sample['name'])
        self.assertEqual(res.data['genre']['is_income'], sample['is_income'])
        self.assertEqual(res.data['genre']['fund'], sample['fund'])
        self.assertEqual(res.data['token'], self.token)

    def test_delete(self):
        sample = self.samples['genres'][0][0]
        self.create_genre(self.user, sample, self.fund)
        res = self.api_request(BY_ID_1_URL, 'DELETE', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('genre', res.data)
        self.assertEqual(res.data['genre'], {})
        self.assertEqual(res.data['token'], self.token)
