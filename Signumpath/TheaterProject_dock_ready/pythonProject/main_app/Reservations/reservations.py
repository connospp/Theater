from flask import request, Blueprint
from main_app.Theaters.theaters import Theaters
from main_app.models import Reservations, Movies
from config import db
from main_app.Reservations.booking import Booking_work

reservations_bp = Blueprint('reservations', __name__)  # reservations endpoint reaches here
res = Booking_work(db, Reservations)  # initialize booking_work class with its inherits


@reservations_bp.route('/delete_booking/<booking_id>', methods=['GET', 'DELETE'])  # method to delete booking
def delete_reservation(booking_id):
    if request.method == 'GET':
        return 'Enter your reservation ID to delete your booking'

    elif request.method == 'DELETE':
        all_reservations = Reservations.query.filter_by(
            reservation_number=booking_id).all()  # gets all reservations with UID
        if len(all_reservations) == 0:  # if UID not exist return message
            return 'Cannot find reservation with this ID. Please check and try again'

        else:
            return res.delete_all_with_id(booking_id)  # Procees with deleting


@reservations_bp.route('/<movieid>/<theaterid>', methods=['POST'])
def book_seats(movieid, theaterid):  # When theater and movie is selected Post method goes here
    movie = Movies.query.get_or_404(movieid)
    theater = Theaters.query.get_or_404(theaterid)

    asking_seats = request.json['seats']  # JSON file must show with selected seats

    if len(asking_seats) < 1:  # If not seats selected returns message
        return "Cannot book less than 1 seat"

    return res.start_booking(asking_seats, movie, theater)  # start booking


@reservations_bp.route('/<movieid>/<theaterid>',methods=['GET'])  # When theater and movie selected get goes here
def see_seats(movieid, theaterid):  # We show how many and which seats are available
    movie = Movies.query.get_or_404(movieid)
    theater = Theaters.query.get_or_404(theaterid)
    available_seats = res.find_empty_seats(theaterid, movie.name) # Access db for unreserved seats
    available_number_of_seats = len(available_seats)

    return {"movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
            "theater_address": theater.address, "available_tickets": available_number_of_seats,
            "available_seats": str(available_seats)}
