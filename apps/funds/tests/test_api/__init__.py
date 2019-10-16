from funds.tests import FundsTests
from core.tests import APITests


class FundsAPITests(FundsTests, APITests):

    namespace = 'fund'

    def setUp(self):
        FundsTests.setUp(self)
        APITests.setUp(self)
