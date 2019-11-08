from funds.tests.test_api import FundsAPITests
from core.tests.test_api.private import OwnerPrivateAPITests, AdminPrivateAPITests


class OwnerPrivateFundsAPITests(FundsAPITests, OwnerPrivateAPITests):
    '''Test funds API requests that require owner authentication.'''

    def setUp(self):
        FundsAPITests.setUp(self)
        OwnerPrivateAPITests.setUp(self)


class AdminPrivateFundsAPITests(FundsAPITests, AdminPrivateAPITests):
    '''Test funds API requests that require admin authentication.'''

    def setUp(self):
        FundsAPITests.setUp(self)
        AdminPrivateAPITests.setUp(self)


class ListAPITests:
    '''Test list requests to funds API.'''

    def setUp(self):
        for sample in self.samples['funds'][0]:
            self.create_fund(self.user, sample)
        for sample in self.samples['funds'][1]:
            self.create_fund(self.user2, sample)
