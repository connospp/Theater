import unittest
import requests
import random
from config import db
from main_app.models import Reservations, Theaters, Movies


class EndToEndTest_7(unittest.TestCase):
    URL = "http://127.0.0.1:5000"

    all_seats = ('A1', 'A2', 'A3', 'A4',  # A tuple of the seating arrangments
                 'B1', 'B2', 'B3', 'B4',
                 'C1', 'C2', 'C3', 'C4',
                 'D1', 'D2', 'D3', 'D4',
                 'E1', 'E2', 'E3', 'E4')

    def setUp(self):  # Setup for each test case
        Reservations.query.delete() #clear reservation table
        db.session.commit()

    def tearDown(self):  # Teardown after each test case
        Reservations.query.delete() #clear reservation table
        db.session.commit()

    def test_one_of_batch_already_reserved(self):  # Send a batch reservation, where on is already reserved
        booking_url = self.URL + "/reservations/1/1"
        seats_to_book = ['A1']
        resp = requests.post(booking_url, json={"seats": seats_to_book})  # Book A1 seat
        self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()
        self.assertEqual(table_size, 1)  # Verify reservation went through

        seats_to_book = random.sample(self.all_seats, 5)  # Select 5 random seats from tuple
        seats_to_book.append('A1')  # Append already reserved seat to the end of list

        resp = requests.post(booking_url, json={"seats": seats_to_book})  # Try to book
        self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()

        self.assertEqual(table_size, 1)  # Make sure second reservation was canceled.

    def test_one_of_batch_none_existent(self):  # Send a batch reservation, where one is a none existing seat
        booking_url = self.URL + "/reservations/1/1"

        seats_to_book = random.sample(self.all_seats, 5)  # Select 5 random seats from tuple
        seats_to_book.append('G1')  # Append G1 to the end (not part of seating arrangments)

        resp = requests.post(booking_url, json={"seats": seats_to_book})
        self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()  # Check reservation table

        self.assertEqual(table_size, 0)  # No booking was made

    def test_one_movie_full_other_still_book(self):  # Make sure that all tables can get full
        theater_table_size = db.session.query(Theaters).count()  # All theaters available
        movie_table_size = db.session.query(Movies).count()  # All movies available

        for theater in range(1, theater_table_size + 1):  # Book all theaters
            for movie in range(1, theater_table_size + 1):  # For all movies
                booking_url = self.URL + f"/reservations/{theater}/{movie}"
                seats_to_book = random.sample(self.all_seats, 20)
                resp = requests.post(booking_url, json={"seats": seats_to_book})
                self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()

        self.assertEqual(table_size, theater_table_size * movie_table_size * len(self.all_seats)) # Make sure all reservations went through
