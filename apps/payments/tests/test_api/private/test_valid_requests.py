from unittest import skip  # noqa: F401
from rest_framework import status

from payments.tests.test_api import ROOT_URL, BY_ID_1_URL, LIST_URL

from . import AdminPrivatePaymentsAPITests, OwnerPrivatePaymentsAPITests


class AdminRequests(AdminPrivatePaymentsAPITests):
    '''Test owner's valid requests to payments API.'''

    # Signed admin has id > 1 other than owner's id in samples (funds, genres, payments)

    def assert_data(self, res, sample):
        self.assertIn('payment', res.data)
        self.assertEqual(res.data['payment']['user']['id'], sample['user']['id'])
        self.assertEqual(res.data['payment']['date'], sample['date'])
        self.assertEqual(res.data['payment']['genre']['id'], sample['genre']['id'])
        sample['incoming'] = sample['incoming'] if sample['incoming'] else 0
        sample['outgoing'] = sample['outgoing'] if sample['outgoing'] else 0
        self.assertEqual(res.data['payment']['incoming'], sample['incoming'])
        self.assertEqual(res.data['payment']['outgoing'], sample['outgoing'])
        sample['remarks'] = sample['remarks'] if sample['remarks'] else ''
        self.assertEqual(res.data['payment']['remarks'], sample['remarks'])
        self.assertEqual(res.data['payment']['fund']['id'], sample['fund']['id'])
        self.assertIn(f"/payments/{res.data['payment']['id']}/", res.data['payment']['url'])
        self.assertEqual(res.data['token'], self.token)

    def test_post(self):
        sample = self.samples['payments'][11]
        res = self.api_request(ROOT_URL, 'POST', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assert_data(res, sample)

    def test_get(self):
        sample = self.samples['payments'][11]
        self.create_payment(**sample)

        res = self.api_request(BY_ID_1_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assert_data(res, sample)

    def test_patch(self):
        sample = self.samples['payments'][11]
        self.create_payment(**sample)
        sample = self.samples['payments'][12]

        res = self.api_request(BY_ID_1_URL, 'PATCH', payload=sample, token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assert_data(res, sample)

    def test_delete(self):
        sample = self.samples['payments'][11]
        self.create_payment(**sample)

        res = self.api_request(BY_ID_1_URL, 'DELETE', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payment', res.data)
        self.assertEqual(res.data['payment'], {})
        self.assertEqual(res.data['token'], self.token)


class OwnerRequest(OwnerPrivatePaymentsAPITests, AdminRequests):
    '''Test owner's valid requests to payments API.'''

    # Signed user has id = 1 same with owner's id in samples (funds, genres, payments)


class AdminGetList(AdminPrivatePaymentsAPITests):
    '''Test admin's list requests to payments API.'''

    def setUp(self):
        super().setUp()
        self.create_payments(self.samples['payments'])

    def test_get_list(self):
        res = self.api_request(LIST_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), len(self.samples['payments']))
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_user_id(self):
        res = self.api_request(LIST_URL + '?filters=user_id:1', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertTrue(len(res.data['payments']) > 0)
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_date(self):
        res = self.api_request(LIST_URL + '?filters=date:01-11-2019 30-11-2019', 'GET', token=self.token)  # noqa: E501

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), 4)
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_incoming(self):
        res = self.api_request(LIST_URL + '?filters=incoming:20', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), 1)
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_outgoing(self):
        res = self.api_request(LIST_URL + '?filters=outgoing:0.01 19.9', 'GET', token=self.token)  # noqa: E501

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), 2)
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_remarks(self):
        res = self.api_request(LIST_URL + '?filters=remarks:blabla', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), 0)
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_genre_id(self):
        res = self.api_request(LIST_URL + '?filters=genre_id:100', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), 0)
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_filters_fund_id(self):
        res = self.api_request(LIST_URL + '?filters=fund_id:200', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertEqual(len(res.data['payments']), 0)
        self.assertEqual(res.data['token'], self.token)


class OwnerGetList(OwnerPrivatePaymentsAPITests):
    '''Test owner's list requests to payments API.'''

    def setUp(self):
        super().setUp()
        self.create_payments(self.samples['payments'])

    def test_get_list(self):
        res = self.api_request(LIST_URL, 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertNotEqual(len(res.data['payments']), len(self.samples['payments']))
        self.assertEqual(res.data['token'], self.token)

    def test_get_list_passing_self_user_id(self):
        res = self.api_request(LIST_URL + '?user_id=1', 'GET', token=self.token)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('payments', res.data)
        self.assertTrue(len(res.data['payments']) > 0)
        self.assertEqual(res.data['token'], self.token)
