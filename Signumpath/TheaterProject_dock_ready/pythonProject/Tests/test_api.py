import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

    def test_1(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
