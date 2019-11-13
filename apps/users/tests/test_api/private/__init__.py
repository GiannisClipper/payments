from .. import UsersAPITests
from core.tests.test_api.private import PrivateAPITests


class UsersPrivateAPITests(UsersAPITests, PrivateAPITests):
    '''Test users API requests that require owner (simple user) authentication.'''

    def setUp(self):
        UsersAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        self.create_admins(self.samples['admins'])
        self.create_users(self.samples['users'])
