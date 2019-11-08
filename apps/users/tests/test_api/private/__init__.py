from .. import UsersAPITests
from core.tests.test_api.private import PrivateAPITests


class PrivateUsersAPITests(UsersAPITests, PrivateAPITests):
    '''Test users API requests that require authentication.'''
