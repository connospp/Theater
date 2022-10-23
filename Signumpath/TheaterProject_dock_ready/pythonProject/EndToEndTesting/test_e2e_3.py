import unittest
import requests
from config import db
from main_app.models import Movies


class EndToEndTest_3(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

    def test_movies_page_text(self):  # Movies page shows all available movies (name and gender)
        resp = requests.get(self.URL + "/movies")
        table_size = db.session.query(Movies).count()

        for pointer in range(1, table_size + 1):
            self.assertIn(Movies.query.get_or_404(pointer).name, str(resp.content))
            self.assertIn(Movies.query.get_or_404(pointer).gender, str(resp.content))

    def test_movies_page_response(self):  # Movies page response code
        resp = requests.get(self.URL + "/movies")
        self.assertEqual(resp.status_code, 200)
