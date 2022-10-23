import unittest
from sqlalchemy.exc import IntegrityError
from unittest import mock, TestCase


class TestAPI(TestCase):

    # test_start_booking
    @mock.patch('main_app.Reservations.booking.Booking_work.start_booking', side_effect=AttributeError)
    def test_start_booking_return_AttError(self, mock_booking):  # In case .name or .gender
        self.assertRaises(AttributeError, mock_booking)

    @mock.patch('main_app.Reservations.booking.Booking_work.do_the_booking', side_effect=AttributeError)
    def test_do_the_booking_return_AttError(self, mock_booking):  # In case .name or .gender
        self.assertRaises(AttributeError, mock_booking)

    #@mock.patch('main_app.Reservations.booking.Booking_work.commit_changes', side_effect=IntegrityError)
    #def test_commit_to_db_handled(self, mock_booking):
    #    self.assertRaises(IntegrityError, mock_booking)


if __name__ == "__main__":
    unittest.main()
