from django.urls import reverse

from genres.tests import GenresTests
from core.tests.test_api import APITests

SIGNIN_URL = reverse('users:signin')
ROOT_URL = reverse('genres:root')
BY_ID_1_URL = reverse('genres:by-id', kwargs={'id': 1})
BY_ID_2_URL = reverse('genres:by-id', kwargs={'id': 2})
BY_ID_3_URL = reverse('genres:by-id', kwargs={'id': 3})
#LIST_URL = reverse('genres:list')


class GenresAPITests(GenresTests, APITests):

    namespace = 'genre'

    def setUp(self):
        GenresTests.setUp(self)
        APITests.setUp(self)