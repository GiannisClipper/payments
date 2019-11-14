from genres.tests.test_api import GenresAPITests
from core.tests.test_api.private import PrivateAPITests


class AdminPrivateGenresAPITests(GenresAPITests, PrivateAPITests):
    '''Test genres API requests that require admin authentication.'''

    def setUp(self):
        GenresAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        sample = self.samples['admins'][2]
        self.user, self.token = self.signin(sample)


class OwnerPrivateGenresAPITests(GenresAPITests, PrivateAPITests):
    '''Test genres API requests that require owner authentication.'''

    def setUp(self):
        GenresAPITests.setUp(self)
        PrivateAPITests.setUp(self)

        sample = self.samples['users'][1]
        self.user, self.token = self.signin(sample)
