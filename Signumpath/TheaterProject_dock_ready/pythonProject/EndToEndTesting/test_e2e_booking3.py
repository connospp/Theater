import time
import unittest
import requests
import random
from config import db
from main_app.models import Reservations


class EndToEndTest_6(unittest.TestCase):
    URL = "http://127.0.0.1:5000/reservations/1/1"

    all_seats = ('A1', 'A2', 'A3', 'A4',  # Seating arrangement tuple
                 'B1', 'B2', 'B3', 'B4',
                 'C1', 'C2', 'C3', 'C4',
                 'D1', 'D2', 'D3', 'D4',
                 'E1', 'E2', 'E3', 'E4')

    def setUp(self):  # Setup for each test
        Reservations.query.delete()  # clear reservation table
        db.session.commit()

    def tearDown(self):  # Setup for each test
        Reservations.query.delete()  # clear reservation table
        db.session.commit()

    def test_try_duplicate_seat(self):  # Try to book same 2 available seats
        booking_url = self.URL

        seats_to_book = ['A1', 'A1']  # Book A1 twice
        resp = requests.post(booking_url, json={"seats": seats_to_book})
        self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()  # Get table size

        self.assertEqual(table_size, 0)  # Make sure reservation  didn't go through

    def test_try_reserved_seat(self):  # Try to book san already reserved seat
        booking_url = self.URL
        seats_to_book = random.sample(self.all_seats, 5)  # Book 5 random seats
        resp = requests.post(booking_url, json={"seats": seats_to_book})
        self.assertEqual(resp.status_code, 200)  # Response message OK
        time.sleep(0.25)
        resp = requests.post(booking_url, json={"seats": seats_to_book})  # Try to book them again
        self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()

        self.assertEqual(table_size, len(seats_to_book))  # Make sure one 5 seats exist in table. Second reservation
        # must be canceled

    def test_try_not_exist_seat(self):  # Try to book none existing seat
        booking_url = self.URL
        seats_to_book = ['F1']  # Book A1 twice which does not exist in neither theater
        resp = requests.post(booking_url, json={"seats": seats_to_book})
        self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()

        self.assertEqual(table_size, 0)  # Reservation didnt go through
