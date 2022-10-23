from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

all_seats = ('A1', 'A2', 'A3', 'A4',
             'B1', 'B2', 'B3', 'B4',
             'C1', 'C2', 'C3', 'C4',
             'D1', 'D2', 'D3', 'D4',
             'E1', 'E2', 'E3', 'E4')

theaters_size = 20


class Theaters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.address}"


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.gender}"


class Reservations(db.Model):
    __table_args__ = (
                         db.UniqueConstraint('reservation', 'theaterID', 'movie_name')),
    id = db.Column(db.Integer, primary_key=True)
    movieID = db.Column(db.Integer, nullable=False)
    movie_name = db.Column(db.String(), nullable=False)
    theaterID = db.Column(db.Integer, nullable=False)
    reservation = db.Column(db.String(3), nullable=False)
    reservation_number = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"{self.movieID} -{self.movie_name} - {self.theaterID} -  {self.reservation}"


@app.route('/')
def index():
    return 'Welcome to Theater Cyprus'


@app.route('/theaters')
def get_theaters():
    theaters = Theaters.query.all()

    output = []
    for theater in theaters:
        theater_data = {'name': theater.name, 'address': theater.address}
        output.append(theater_data)

    return {"theaters": output}


@app.route('/theaters/<id>')
def get_theater(id):
    theater = Theaters.query.get_or_404(id)
    return ({"name": theater.name, "address": theater.address})


@app.route('/movies')
def get_movies():
    movies = Movies.query.all()
    output = []
    for movie in movies:  # Show all available movie
        movie_data = {'name': movie.name, 'gender': movie.gender}
        output.append(movie_data)

    return {"movies": output}


@app.route('/movies/<id>')
def get_movie(id):
    movie = Movies.query.get_or_404(id)

    theaters = Theaters.query.all()

    output = []
    for theater in theaters:  # Show which theaters you can see this movie
        theater_data = {'name': theater.name, 'address': theater.address}
        output.append(theater_data)

    return {"name": movie.name, "gender": movie.gender, "theaters": output}


@app.route('/delete_booking', methods=['GET', 'DELETE'])
def delete_reservation():
    if request.method == 'GET':
        return 'Enter your reservation ID to see/edit/delete your booking'

    elif request.method == 'DELETE':
        reservation_id = request.json['ID']

        all_reservations = Reservations.query.filter_by(reservation_number=reservation_id).all()

        if len(all_reservations) == 0:
            return 'Cannot find reservation with this ID. Please check and try again'

        else:
            return delete_all_with_id(reservation_id)


@app.route('/movies/<movieid>/<theaterid>', methods=['GET', 'POST'])
def see_and_reserve_seats(movieid, theaterid):
    movie = Movies.query.get_or_404(movieid)
    theater = Theaters.query.get_or_404(theaterid)

    available_seats = find_empty_seats(theaterid, movie.name)
    available_number_of_seats = len(available_seats)

    if request.method == 'GET':  # Show available seats for selected movie
        return {"movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
                "theater_address": theater.address, "available_tickets": str(available_number_of_seats),
                "available_seats": str(available_seats)}

    elif request.method == 'POST':  # Reserve system
        asking_seats = request.json['seats']
        res_ID = generate_unique_res_id()  # default ID

        if len(asking_seats) < 1:
            return "Cannot book less than 1 seat"

        for new_seat in range(len(asking_seats)):
            row_to_add = Reservations(movieID=movieid, movie_name=movie.name, theaterID=theaterid,
                                      reservation=asking_seats[new_seat], reservation_number=res_ID)
            db.session.add(row_to_add)

        try:
            db.session.commit()

        except exc.IntegrityError:
            db.session.rollback()
            available_seats = find_empty_seats(theaterid, movie.name)
            available_number_of_seats = len(available_seats)

            return {"message": "Something wrong with seat selection possible issue, duplicate seat selection,selected "
                               "seat not available any more, invalid seat selection Select new seats and try again. "
                               "Make sure all seat selection is unique",
                    "movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
                    "theater_address": theater.address, "available_tickets": str(available_number_of_seats),
                    "available_seats": str(available_seats)}

        return f"Success!!! Booking reference {res_ID}"


def generate_unique_res_id():
    res_ID = 1  # default ID
    does_UID_exists = 1  # check if ID exists

    while does_UID_exists != 0:
        res_ID = str(uuid.uuid4())
        does_UID_exists = len(Reservations.query.filter_by(reservation_number=res_ID).all())

    return res_ID


def find_empty_seats(theaterID, movie_name):
    available_seats_for_show = list(all_seats)
    made_reservations = Reservations.query.filter_by(movie_name=movie_name).filter_by(theaterID=theaterID).all()
    if len(made_reservations) > 0:
        for reserve in made_reservations:
            available_seats_for_show.remove(reserve.reservation)

    return available_seats_for_show


def delete_all_with_id(resID):
    Reservations.query.filter_by(reservation_number=resID).delete()
    all_reservations = Reservations.query.filter_by(reservation_number=resID).all()

    if len(all_reservations) == 0:
        db.session.commit()
        message = "Reservation successfully deleted."

    else:
        db.session.rollback()
        message = "Something went wrong. Please try again contact customer support with yout reservation number"

    return message

    # available_number_of_seats = len(all_seats) - len(Reservations.query.filter_by(movie_name=movie.name).filter_by(
    #    theaterID=idt).all())  # Making sure number up to date

    # if available_number_of_seats >= 0:
    #    for reserve in made_reservations:
    #        if reserve.reservation == "TMP": continue
    #        available_seats.remove(reserve.reservation)

    # else:  # if no availability delete
    #    for p in range(booking_number):  # Adding temporary rows
    #        to_Delete = Reservations.query.filter_by(movie_name=movie.name).filter_by(
    #            theaterID=idt).filter_by(reservation="TMP").first()
    #        db.session.delete(to_Delete)
    #        db.session.commit()
    #        available_number_of_seats += 1
    #    return f"Not enough availability. Available tickets {available_number_of_seats}"

    # return {"message": "Reservation made. You have 1 minute to select seats and complete your booking",
    #         "movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
    #         "theater_address": theater.address, "available_tickets": str(len(available_seats)),
    #         "available_seats": str(available_seats)}

    # Reservations.query.filter_by(id=resID).update(dict(av_Seats=available_seats - booking_number))
    # db.session.commit()
    # available_seats = Reservations.query.get_or_404(resID).av_Seats  # Making sure number up to date

    # if available_seats >= 0:
    #    return f"You have successfully reserve {booking_number} tickets for 1 minute." \
    #           f" Please proceed with selecting your seats to complete reservation"

    # else:
    #    Reservations.query.filter_by(id=resID).update(dict(av_Seats=available_seats + booking_number))
    #    db.session.commit()
    #    available_seats = Reservations.query.get_or_404(resID).av_Seats
    #    return f"Not enough availability to book {booking_number} tickets. Current availability {available_seats}"

    # resID = int(f"{idm}{idt}")
    # reservation = Reservations.query.get(resID)

    # if reservation.movie_name != movie.name:
    #    Reservations.query.filter_by(id=resID).delete()

    # if reservation is None or reservation.movie_name != movie.name:
    #    row_to_add = Reservations(id=resID, movieID=idm, movie_name=movie.name, theaterID=idt, av_Seats=20)
    #    db.session.add(row_to_add)
    #    db.session.commit()

    # available_seats = Reservations.query.get_or_404(resID).av_Seats

    # if request.method == 'GET':
    #    return {"movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
    #            "theater_address": theater.address, "available_Seats": available_seats}

    # elif request.method == 'POST':
    #    booking_number = request.json['number']

    # if booking_number <= 0:
    #        return "Booking number must be higher than 0"

    #    available_seats = Reservations.query.get_or_404(resID).av_Seats  # Making sure number up to date
    #    Reservations.query.filter_by(id=resID).update(dict(av_Seats=available_seats - booking_number))
    #     db.session.commit()
    #     available_seats = Reservations.query.get_or_404(resID).av_Seats  # Making sure number up to date

    #    if available_seats >= 0:
    #        return f"You have successfully reserve {booking_number} tickets for 1 minute." \
    #              f" Please proceed with selecting your seats to complete reservation"

    #    else:
    #        Reservations.query.filter_by(id=resID).update(dict(av_Seats=available_seats + booking_number))
    #        db.session.commit()
    #        available_seats = Reservations.query.get_or_404(resID).av_Seats
    #        return f"Not enough availability to book {booking_number} tickets. Current availability {available_seats}"

# @main_app.route('/movies/<idm>/<idt>', methods=['GET'])
# def get_seats(idm, idt):
#     movie = Movies.query.get_or_404(idm)
#     theater = Theaters.query.get_or_404(idt)
#     table_name = f"{movie.name}@{theater.name}"
#
#     engine = sqlalchemy.create_engine('sqlite:///seats.db')  # Create seats db
#     connection = engine.connect()
#     metadata = sqlalchemy.MetaData()
#
#     active_table = sqlalchemy.Table(table_name, metadata,
#                                     sqlalchemy.Column('Seat', sqlalchemy.String(3), nullable=False),
#                                     sqlalchemy.Column('Id', sqlalchemy.Integer()))
#
#     def available_seats():
#         dataSeats = sqlalchemy.Table('table_name', metadata)
#         query = sqlalchemy.select(active_table)
#         ResultProxy = connection.execute(query)
#         return str(ResultProxy.fetchall()).replace(',', '')
#
#     all_tables = engine.table_names()
#     for table in all_tables:
#         if table == table_name:
#             return {"movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
#                     "theater_address": theater.address, "available_Seats": str(available_seats())}
#
#     metadata.create_all(engine)  # Creates the table
#
#     query = sqlalchemy.insert(active_table)
#     values_to_add = [{'Seat': "A1", 'Id': 1}, {'Seat': "A2", 'Id': 2}, {'Seat': "A3", 'Id': 3}, {'Seat': "A4", 'Id': 4},
#                      {'Seat': "B1", 'Id': 5}, {'Seat': "B2", 'Id': 6}, {'Seat': "B3", 'Id': 7}, {'Seat': "B4", 'Id': 8},
#                      {'Seat': "C1", 'Id': 9}, {'Seat': "C2", 'Id': 10}, {'Seat': "C3", 'Id': 11},
#                      {'Seat': "C4", 'Id': 12},
#                      {'Seat': "D1", 'Id': 13}, {'Seat': "D2", 'Id': 14}, {'Seat': "D3", 'Id': 15},
#                      {'Seat': "D4", 'Id': 16},
#                      {'Seat': "E1", 'Id': 17}, {'Seat': "E2", 'Id': 18}, {'Seat': "E3", 'Id': 19},
#                      {'Seat': "E4", 'Id': 20}]
#
#     ResultProxy = connection.execute(query, values_to_add)
#
#     return {"movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
#             "theater_address": theater.address, "available_Seats": str(available_seats())}
#
#
# @main_app.route('/movies/<idm>/<idt>/<ids>')
# def reserve_seats(idm, idt):
#     movie = Movies.query.get_or_404(idm)
#     theater = Theaters.query.get_or_404(idt)
#     table_name = f"{movie.name}@{theater.name}"
#
#     engine = sqlalchemy.create_engine('sqlite:///seats.db')  # Create seats db
#     connection = engine.connect()
#     metadata = sqlalchemy.MetaData()
#
#     active_table = sqlalchemy.Table(table_name, metadata,
#                                     sqlalchemy.Column('Seat', sqlalchemy.String(3), nullable=False),
#                                     sqlalchemy.Column('Id', sqlalchemy.Integer()))
#
#
#
#     return {"movie_name": movie.name, "movie_gender": movie.gender, "theater_name": theater.name,
#             "theater_address": theater.address}

# @main_app.route('/drinks', methods=['POST'])
# def add_drink():
#    drink = Drink(name=request.json['name'], description=request.json['description'])
#    db.session.add(drink)
#    db.session.commit()
#    return {'id': drink.id}


# @main_app.route('/drinks/<id>', methods=['DELETE'])
# def delete_drink(id):
#    drink = Drink.query.get(id)
#    if drink is None:
#        return {"error": "not found"}
#    db.session.delete(drink)
#    db.session.commit()
#    return {"message": "yeehgaaa"}
