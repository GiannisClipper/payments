from users.tests import UsersTests
from core.tests.test_api import APITests


class UsersAPITests(UsersTests, APITests):

    namespace = 'user'

    def setUp(self):
        UsersTests.setUp(self)
        APITests.setUp(self)
