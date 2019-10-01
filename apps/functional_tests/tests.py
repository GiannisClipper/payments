from django.test import LiveServerTestCase
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

from apps.constants import WELCOME, SIGNATURE, LINKEDIN_URL, GITHUB_URL


class RootRequestTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_root_response(self):
        # self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        self.assertIn(WELCOME, self.browser.page_source)
        self.assertIn(SIGNATURE, self.browser.page_source)
        self.assertIn(LINKEDIN_URL, self.browser.page_source)
        self.assertIn(GITHUB_URL, self.browser.page_source)
