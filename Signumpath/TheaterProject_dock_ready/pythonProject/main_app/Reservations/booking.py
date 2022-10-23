from sqlalchemy.exc import IntegrityError
from main_app.Reservations.reservation_utils import Reservation_work


class Booking_work(Reservation_work):  # Inherits everything from reservation_work

    def start_booking(self, asking_seats, movie, theater):  # Start booking
        success = self.do_the_booking(asking_seats, movie, theater)  # execute booking

        if success == 0:  # If unsuccessfully shows message and current available seats
            self.db.session.rollback()  # If unsuccessful commit, we roll back changes
            available_seats = self.find_empty_seats(theater.id, movie.name)  # Check db for unreserved seats
            message = {
                "message": "Invalid seat selection", "movie_name": movie.name,
                "movie_gender": movie.gender, "theater_name": theater.name,
                "theater_address": theater.address, "available_tickets": len(available_seats),
                "available_seats": str(available_seats)}

        else:
            message = f"Success!!! Booking reference {success}"  # If successful, show message and reservation UID

        return message  # Booking message

    def do_the_booking(self, asking_seats, movie, theater):  # Does the actual booking
        res_ID = self.generate_unique_res_id()  # generates default ID that we make sure it is not present in db

        for new_seat in range(len(asking_seats)):  # iterating through asking seats
            row_to_add = self.resr(movieID=movie.id, movie_name=movie.name, theaterID=theater.id,
                                   reservation=asking_seats[new_seat], reservation_number=res_ID)
            self.db.session.add(row_to_add)  # Push to db buffer. Wont be added to db before we commit

            if asking_seats[new_seat] not in self.all_seats:  # If not a valid seat selection we return 'unsuccessful'
                return 0

        return self.commit_changes(res_ID)  # Commit changes to db

    def commit_changes(self, res_ID):  # commit changes to db
        try:
            self.db.session.commit()  # try to commit
            return res_ID  # if successfull return the booking UID

        except IntegrityError:
            return 0  # returns unsuccessful to rollback db
