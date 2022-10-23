import unittest
import requests
import random
from config import db
from main_app.models import Reservations


class EndToEndTest_5(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"

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

    def test_same_seat_same_theater_different_movie(self):  # Try to book same seat different movie same theater
        theater_id = 1
        movies_id = [1, 2]  # Movies to book seat

        seats_to_book = random.sample(self.all_seats, 1)  # Select a random seat to book
        for id in movies_id:  # For each movie ID book seat
            booking_url = self.URL + f"reservations/{id}/{theater_id}"
            resp = requests.post(booking_url, json={"seats": seats_to_book})
            self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()  # Get table size to iterate

        for row in range(1, table_size + 1):  # For each row in reservations table
            self.assertEqual(Reservations.query.get_or_404(row).theaterID, theater_id)  # Right theater was booked
            self.assertIn(Reservations.query.get_or_404(row).reservation, seats_to_book)  # Right seat was booked
            self.assertIn(Reservations.query.get_or_404(row).movieID, movies_id)  # Movie ID one of the 2 selected
            movies_id.remove(Reservations.query.get_or_404(row).movieID)  # Remove id from list to verify all present

        self.assertEqual(len(movies_id), 0)  # Verify all available movies were found in table and removed from list

    def test_same_seat_same_movie_different_theater(self):  # Try to book same seat different theater same movie
        movies_id = 1
        theater_id = [1, 2]  # Theaters to book a seat

        seats_to_book = random.sample(self.all_seats, 1)  # Select a random seat to book
        for id in theater_id:  # For each theater ID book seat
            booking_url = self.URL + f"reservations/{movies_id}/{id}"
            resp = requests.post(booking_url, json={"seats": seats_to_book})
            self.assertEqual(resp.status_code, 200)  # Response message OK

        table_size = db.session.query(Reservations).count()  # Get table size to iterate

        for row in range(1, table_size + 1):  # For each row in reservations table
            self.assertEqual(Reservations.query.get_or_404(row).movieID, movies_id)  # Right movie was booked
            self.assertIn(Reservations.query.get_or_404(row).reservation, seats_to_book)  # Right seat was booked
            self.assertIn(Reservations.query.get_or_404(row).theaterID, theater_id)  # Theatre ID one of the 2 selected
            theater_id.remove(Reservations.query.get_or_404(row).theaterID)  # Remove id from list to verify all present

        self.assertEqual(len(theater_id), 0)  # Verify all available theaters were found in table and removed from list
