import unittest
import requests

class EndToEndTest(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

    def test_landing_page_text(self):  # Landing page message shown
        resp = requests.get(self.URL)
        self.assertEqual(resp.content, b'Welcome to Theater Cyprus')

    def test_landing_page_status(self):  # Landing page response code
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
