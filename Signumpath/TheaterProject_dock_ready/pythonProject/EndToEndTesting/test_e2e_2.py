import unittest
import requests
from config import db
from main_app.models import Theaters


class EndToEndTest_2(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

    def test_theaters_page_text(self): # Loading all theaters shows all necessary details (address and name)
        resp = requests.get(self.URL + "/theaters")
        table_size = db.session.query(Theaters).count()

        for pointer in range(1, table_size + 1):
            self.assertIn(Theaters.query.get_or_404(pointer).name, str(resp.content)) # Make sure we show name of each theater in db
            self.assertIn(Theaters.query.get_or_404(pointer).address, str(resp.content)) # Make sure we show address for each theater in db

    def test_theaters_page_response(self): # Theaters page loads successfully
        resp = requests.get(self.URL + "/theaters")
        self.assertEqual(resp.status_code, 200)
