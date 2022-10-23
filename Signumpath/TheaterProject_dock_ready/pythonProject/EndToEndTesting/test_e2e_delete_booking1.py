import unittest
import requests
import random
from config import db
from main_app.models import Reservations


class EndToEndTest_8(unittest.TestCase):
    URL = "http://127.0.0.1:5000"

    all_seats = ('A1', 'A2', 'A3', 'A4',  # A tuple of the seating arrangments
                 'B1', 'B2', 'B3', 'B4',
                 'C1', 'C2', 'C3', 'C4',
                 'D1', 'D2', 'D3', 'D4',
                 'E1', 'E2', 'E3', 'E4')

    def setUp(self):  # Setup for each test case
        Reservations.query.delete()  # clear reservation table
        db.session.commit()

    def tearDown(self):  # Teardown for each test case
        Reservations.query.delete()  # clear reservation table
        db.session.commit()

    def test_get_delete_endpoint(self):  # Get delete end point verify string
        delete_url = self.URL + f"/reservations/delete_booking/xxx"
        resp = requests.get(delete_url)

        self.assertEqual(resp.content, b'Enter your reservation ID to delete your booking')

    def test_delete_reservation(self):  # Verify we can delete reservation
        booking_url = self.URL + "/reservations/1/1"

        seats_to_book = random.sample(self.all_seats, 6)  # Select 6 random seats to book
        first_seat = [seats_to_book[0]]  # First book individually first item in list

        resp = requests.post(booking_url, json={"seats": first_seat})
        self.assertEqual(resp.status_code, 200)  # Response OK

        seats_to_book.remove(seats_to_book[0])  # Remove for string to avoid double booking cancellation

        resp = requests.post(booking_url, json={"seats": seats_to_book})  # Book remaining seats in list
        self.assertEqual(resp.status_code, 200)  # Response OK

        booking_reference = str(resp.content).split(' ')[-1].replace("'", '')  # Get booking reference

        delete_url = self.URL + f"/reservations/delete_booking/{booking_reference}"  # Enter in the delete URL

        resp = requests.delete(delete_url)  # Send delete order
        self.assertEqual(resp.status_code, 200)  # Response OK

        table_size = db.session.query(Reservations).count()

        self.assertEqual(resp.content, b'Reservation successfully deleted.')  # Verification message
        self.assertEqual(table_size, 1)  # Verify table only contains first reservation made independently

    def test_delete_reservation_invalid_bookingid(self):  # Try to delete with invalid booking
        delete_url = self.URL + f"/reservations/delete_booking/xxx"  # Try delete booking xxx
        resp = requests.delete(delete_url)
        self.assertEqual(resp.status_code, 200)  # Response OK

        self.assertEqual(resp.content, b'Cannot find reservation with this ID. Please check and try again')
