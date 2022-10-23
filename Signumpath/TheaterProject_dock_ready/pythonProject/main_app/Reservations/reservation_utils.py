import uuid


class Reservation_work:
    all_seats = ('A1', 'A2', 'A3', 'A4',
                 'B1', 'B2', 'B3', 'B4',
                 'C1', 'C2', 'C3', 'C4',
                 'D1', 'D2', 'D3', 'D4',
                 'E1', 'E2', 'E3', 'E4')

    def __init__(self, db, reservation_db):  # Init reservation work and booking
        self.db = db
        self.resr = reservation_db

    def generate_unique_res_id(self):  # Generate UID and make sure it is not present in dbS
        res_ID = 1  # default ID
        does_UID_exists = 1  # check if ID exists
        while does_UID_exists != 0:
            res_ID = str(uuid.uuid4())
            does_UID_exists = len(self.resr.query.filter_by(reservation_number=res_ID).all())
        return res_ID  # Return UID

    def find_empty_seats(self, theaterID, movie_name):  # Check db for empty seats
        available_seats_for_show = list(self.all_seats)  # Load all seats from tuple
        made_reservations = self.resr.query.filter_by(movie_name=movie_name).filter_by(theaterID=theaterID).all()
        # Get all reservations for that movie at that theaters
        if len(made_reservations) > 0:  # if reservations exists, iterate to see seats
            for reserve in made_reservations:
                available_seats_for_show.remove(reserve.reservation)
        return available_seats_for_show # return available seats

    def delete_all_with_id(self, resID): # delete all with UID
        self.resr.query.filter_by(reservation_number=resID).delete() # Find and delete all with UID
        all_reservations = self.resr.query.filter_by(reservation_number=resID).all() # Check no more exists with UID

        if len(all_reservations) == 0: # If removed
            self.db.session.commit()   # Commit changes
            message = "Reservation successfully deleted."

        else:
            self.db.session.rollback()  # If not, rollback changes and show error message
            message = "Something went wrong. Please try again contact customer support with your reservation number"
        return message
