from django.urls import reverse

from payments.tests import PaymentsTests
from core.tests.test_api import APITests

ROOT_URL = reverse('payments:root')
BY_ID_1_URL = reverse('payments:by-id', kwargs={'id': 1})
BY_ID_2_URL = reverse('payments:by-id', kwargs={'id': 2})
BY_ID_0_URL = reverse('payments:by-id', kwargs={'id': 0})
LIST_URL = reverse('payments:list')


class PaymentsAPITests(PaymentsTests, APITests):

    namespace = 'payment'

    def setUp(self):
        PaymentsTests.setUp(self)
        APITests.setUp(self)
