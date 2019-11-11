from genres.tests.test_api import GenresAPITests
from core.tests.test_api.private import OwnerPrivateAPITests, AdminPrivateAPITests


class OwnerPrivateGenresAPITests(GenresAPITests, OwnerPrivateAPITests):
    '''Test genres API requests that require owner authentication.'''

    def setUp(self):
        GenresAPITests.setUp(self)
        OwnerPrivateAPITests.setUp(self)
        fund_ = self.samples['funds'][0][0]
        self.fund = self.create_fund(self.user, fund_)
        fund_ = self.samples['funds'][0][1]
        self.fund2 = self.create_fund(self.user, fund_)

class AdminPrivateGenresAPITests(GenresAPITests, AdminPrivateAPITests):
    '''Test genres API requests that require admin authentication.'''

    def setUp(self):
        GenresAPITests.setUp(self)
        AdminPrivateAPITests.setUp(self)
