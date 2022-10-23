import unittest
import asyncio
import aiohttp
import random
from config import db
from main_app.models import Reservations


class EndToEndTest_9(unittest.TestCase):
    URL = "http://127.0.0.1:5000/reservations/1/1"

    all_seats = ('A1', 'A2', 'A3', 'A4',  # A tuple of the seating arrangements
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

    def test_multiple_identical_requests(self):  # This test spams the same booking selection 15 times in less than 0.1
        repeat = 15  # Number of times to spam db
        seats_to_book = random.sample(self.all_seats, 5)  # Select 5 random seats to book

        messages = asyncio.run(self.main_spame_same(seats_to_book, repeat))  # Execute async booking

        table_size = db.session.query(Reservations).count()  # Check reservation table size
        self.assertEqual(table_size, 5)  # Make sure duplicate reservations were canceled.
        self.assertEqual(len(messages), repeat)  # Verify 15 messages were received

        success_bookings = 0
        for message in messages:  # Verify only one successfull message was received
            if "Success!!! Booking reference" in str(message):
                success_bookings += 1

        self.assertEqual(success_bookings, 1)

    def test_multiple_different_requests(self):  # 4 Valid batch queries done in async
        batches = [[] for i in range(4)]

        batches[0].extend([self.all_seats[0], self.all_seats[1], self.all_seats[2], self.all_seats[3]])  # 5 bookings
        batches[1].extend([self.all_seats[4], self.all_seats[5], self.all_seats[6], self.all_seats[7]])
        batches[2].extend([self.all_seats[8], self.all_seats[9], self.all_seats[10], self.all_seats[11]])
        batches[3].extend([self.all_seats[12], self.all_seats[13], self.all_seats[14], self.all_seats[15]])

        messages = asyncio.run(self.main(batches, len(batches)))  # Execute bookings

        table_size = db.session.query(Reservations).count()
        self.assertEqual(table_size, 16)  # All 16 reservations went through
        self.assertEqual(len(messages), len(batches))  # Equal messages returned

    async def main_spame_same(self, bookings, repeat):  # Async spam same selection
        async with aiohttp.ClientSession() as session:
            messages = await asyncio.gather(  # Gathers CPU resources
                *[self.do_booking(self.URL, session, bookings) for pointer in range(repeat)])  # Perform bookings
        return messages  # Return collected mesasges

    async def main(self, bookings, repeat):  # Async multiple valid reservations
        async with aiohttp.ClientSession() as session:
            messages = await asyncio.gather(  # Gathers CPU resources
                *[self.do_booking(self.URL, session, bookings[pointer]) for pointer in range(repeat)])
            return messages  # Return collected messages

    async def do_booking(self, url, session, seats):  # Execute async bookings
        async with session.post(url=url, json={"seats": seats}) as response:
            resp = await response.read()
            self.assertEqual(response.status, 200)  # Verify request went through
            return resp  # Return messages
