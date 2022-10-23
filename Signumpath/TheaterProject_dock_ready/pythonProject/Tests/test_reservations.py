import unittest
import requests
from unittest import mock, TestCase


class TestAPI(TestCase):
    URL = "http://127.0.0.1:5000/reservations/"

    # delete_reservation function
    def test_getdelete_reservations_response(self):
        resp = requests.get(self.URL + "delete_booking/xxx")
        self.assertEqual(resp.status_code, 200)

    def test_delete_reservations_response(self):
        resp = requests.delete(self.URL + "delete_booking/xxx")
        self.assertEqual(resp.status_code, 200)

    # book_seats function
    @mock.patch('main_app.Reservations.reservations.book_seats', side_effect=KeyError)
    def test_booking_returns_KeyError(self, mock_booking):  # Empty JSON received
        self.assertRaises(KeyError, mock_booking)

    @mock.patch('main_app.Reservations.reservations.book_seats', side_effect=TypeError)
    def test_booking_returns_TypeError(self, mock_booking):  # No data received
        self.assertRaises(TypeError, mock_booking)

    def test_invalid_movie_and_theater(self):
        resp = requests.post(self.URL + "x/x/")
        self.assertEqual(resp.status_code, 404)

    # see availability
    def test_movie_and_theater(self):
        resp = requests.get(self.URL + "1/1")
        self.assertEqual(resp.status_code, 200)

    def test_check_invalid_movie_and_theater(self):
        resp = requests.get(self.URL + "x/x")
        self.assertEqual(resp.status_code, 404)

    @mock.patch('main_app.Reservations.reservations.see_seats', side_effect=AttributeError)
    def test_see_seats_returns_attrError(self, mock_see_seats):  # In case .name or .gender
        self.assertRaises(AttributeError, mock_see_seats)

    def test_see_seats_response(self):
        resp = requests.get(self.URL + "/1/1")
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
