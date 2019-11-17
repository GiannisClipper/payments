from payments.tests.test_api import PaymentsAPITests
from core.tests.test_api.private import PrivateAPITests


class AdminPrivatePaymentsAPITests(PaymentsAPITests, PrivateAPITests):
    '''Test payments API requests that require admin authentication.'''

    def setUp(self):
        PaymentsAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        sample = self.samples['admins'][2]
        self.user, self.token = self.signin(sample)


class OwnerPrivatePaymentsAPITests(PaymentsAPITests, PrivateAPITests):
    '''Test payments API requests that require owner authentication.'''

    def setUp(self):
        PaymentsAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        sample = self.samples['users'][1]
        self.user, self.token = self.signin(sample)
