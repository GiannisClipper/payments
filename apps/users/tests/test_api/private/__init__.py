from .. import UsersAPITests
from core.tests.test_api.private import PrivateAPITests


class OwnerSigninSupported(UsersAPITests, PrivateAPITests):
    '''Test users API requests that require owner (simple user) authentication.'''

    def setUp(self):
        UsersAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        self.create_users(self.samples['users'])


class AdminSigninSupported(UsersAPITests, PrivateAPITests):
    '''Test users API requests that require admin authentication.'''

    def setUp(self):
        UsersAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        self.create_admins(self.samples['users'])
