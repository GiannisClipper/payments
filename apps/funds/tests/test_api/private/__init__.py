from funds.tests.test_api import FundsAPITests
from core.tests.test_api.private import PrivateAPITests


class AdminPrivateFundsAPITests(FundsAPITests, PrivateAPITests):
    '''Test funds API requests that require admin authentication.'''

    def setUp(self):
        FundsAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        sample = self.samples['admins'][1]
        self.user, self.token = self.signin(sample)


class OwnerPrivateFundsAPITests(FundsAPITests, PrivateAPITests):
    '''Test funds API requests that require owner authentication.'''

    def setUp(self):
        FundsAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        sample = self.samples['users'][1]
        self.user, self.token = self.signin(sample)
