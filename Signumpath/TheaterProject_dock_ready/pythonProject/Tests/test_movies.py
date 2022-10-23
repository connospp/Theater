import unittest
import requests
from unittest import mock, TestCase


class TestAPI(TestCase):
    URL = "http://127.0.0.1:5000/movies"

    # get_movies function
    @mock.patch('main_app.Movies.movies.get_movies', side_effect=AttributeError)
    def test_get_movies_returns_attrError(self, mock_get_movies):  # In case .name or .gender
        self.assertRaises(AttributeError, mock_get_movies)

    def test_get_movies_response(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)

    # get_movie function
    @mock.patch('main_app.Movies.movies.get_movie', side_effect=AttributeError)
    def test_get_movie_returns_attrError(self, mock_get_movie):  # In case .name or .gender
        self.assertRaises(AttributeError, mock_get_movie)

    def test_get_movie_invalid_selection(self):
        resp = requests.get(self.URL + "/0")
        self.assertEqual(resp.status_code, 404)

    def test_get_movie_response(self):
        resp = requests.get(self.URL + "/1")
        self.assertEqual(resp.status_code, 200)

    # redirect to reservation
    def test_get_movie_redirect(self):
        universal_id = 1
        resp = requests.get(self.URL + f"/{universal_id}/{universal_id}")
        current_url = resp.request.path_url
        self.assertEqual(current_url, f"/reservations/{universal_id}/{universal_id}")


if __name__ == "__main__":
    unittest.main()
