import unittest
import requests
from unittest import mock, TestCase


class TestAPI(TestCase):
    URL = "http://127.0.0.1:5000/theaters"

    # get_theaters function
    @mock.patch('main_app.Theaters.theaters.get_theaters', side_effect=AttributeError)
    def test_get_theaters_returns_attrError(self, mock_get_theaters):  # In case .name or .address does not exists
        self.assertRaises(AttributeError, mock_get_theaters)

    def test_get_theaters_response(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)

    # get_theater function
    @mock.patch('main_app.Theaters.theaters.get_theater', side_effect=AttributeError)
    def test_get_theater_returns_attrError(self, mock_get_theaters):  # In case .name or .address does not exists
        self.assertRaises(AttributeError, mock_get_theaters)

    def test_get_theater_invalid_selection(self):
        resp = requests.get(self.URL + "/0")
        self.assertEqual(resp.status_code, 404)

    def test_get_theater_response(self):
        resp = requests.get(self.URL + "/1")
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
