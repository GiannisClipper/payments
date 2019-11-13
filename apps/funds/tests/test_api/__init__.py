from django.urls import reverse

from funds.tests import FundsTests
from core.tests.test_api import APITests

ROOT_URL = reverse('funds:root')
BY_ID_1_URL = reverse('funds:by-id', kwargs={'id': 1})
BY_ID_2_URL = reverse('funds:by-id', kwargs={'id': 2})
BY_ID_0_URL = reverse('funds:by-id', kwargs={'id': 0})
LIST_URL = reverse('funds:list')


class FundsAPITests(FundsTests, APITests):

    namespace = 'fund'

    def setUp(self):
        FundsTests.setUp(self)
        APITests.setUp(self)
