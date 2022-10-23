import unittest
import requests
import random
from config import db
from main_app.models import Reservations


class EndToEndTest_4(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

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

    def test_book_zero_seat(self):  # Try to book seats with 0 selection
        booking_url = self.URL + "reservations/1/1"

        resp = requests.get(booking_url)
        self.assertEqual(resp.status_code, 200)

        resp_post = requests.post(booking_url, json={"seats": []})
        self.assertEqual(resp_post.status_code, 200)

        self.assertEqual(resp_post.content, b'Cannot book less than 1 seat')  # Code can handle this situation

    def test_book_one_seat(self):  # Try to book 1 seat only
        theater_id = 1
        movies_id = 1
        booking_url = self.URL + f"reservations/{movies_id}/{theater_id}"  # booking for movie 1 in theater 1
        seats_to_book = random.sample(self.all_seats, 1)  # Select a random seat to book
        resp_post = requests.post(booking_url, json={"seats": seats_to_book})  # Book that seat
        self.assertEqual(resp_post.status_code, 200)  # Responce message OK

        self.assertEqual(Reservations.query.get_or_404(1).movieID, movies_id)  # Make sure right movie booked
        self.assertEqual(Reservations.query.get_or_404(1).theaterID, theater_id)  # Make sure righ theater booked
        self.assertIn(Reservations.query.get_or_404(1).reservation, seats_to_book)  # Make sure right seat booked
        self.assertIn("Success!!! Booking reference", str(resp_post.content))  # Success message received

    def test_book_five_seat(self):  # Try to book 5 seats at once
        theater_id = 1
        movies_id = 1
        booking_url = self.URL + f"reservations/{movies_id}/{theater_id}"  # Booking for movie 1 in theater 1
        seats_to_book = random.sample(self.all_seats, 5)  # Select 5 random seats to book
        resp_post = requests.post(booking_url, json={"seats": seats_to_book})  # Book all those seats at once
        self.assertEqual(resp_post.status_code, 200)  # Responce message OK

        table_size = db.session.query(Reservations).count()  # Get table size to iterate

        for pointer in range(1, table_size + 1):
            self.assertEqual(Reservations.query.get_or_404(pointer).movieID, movies_id)  # Right movie was booked
            self.assertEqual(Reservations.query.get_or_404(pointer).theaterID, theater_id)  # Right theater was booked
            self.assertIn(Reservations.query.get_or_404(pointer).reservation, seats_to_book)  # Right seats booked
            seats_to_book.remove(Reservations.query.get_or_404(pointer).reservation)  # Remove seat from list. To
            # verify all where booked

        self.assertIn("Success!!! Booking reference", str(resp_post.content))  # Success message shown

    def test_book_twenty_seat(self):  # Try to book 20 seats at once
        theater_id = 1
        movies_id = 1
        booking_url = self.URL + f"reservations/{movies_id}/{theater_id}"  # Booking for movie 1 in theater 1
        seats_to_book = random.sample(self.all_seats, 20)  # Select 20 random seats to book
        resp_post = requests.post(booking_url, json={"seats": seats_to_book})
        self.assertEqual(resp_post.status_code, 200)  # Responce message OK

        table_size = db.session.query(Reservations).count()  # Get table size to iterate

        for pointer in range(1, table_size + 1):
            self.assertEqual(Reservations.query.get_or_404(pointer).movieID, movies_id)  # Right movie was booked
            self.assertEqual(Reservations.query.get_or_404(pointer).theaterID, theater_id)  # Right theater was booked
            self.assertIn(Reservations.query.get_or_404(pointer).reservation, seats_to_book)  # Right seats booked
            seats_to_book.remove(Reservations.query.get_or_404(pointer).reservation)  # Remove seat from list. To
            # verify all where booked

        self.assertIn("Success!!! Booking reference", str(resp_post.content))  # Success message shown
