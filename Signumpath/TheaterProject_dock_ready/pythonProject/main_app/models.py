from config import db

class Theaters(db.Model):  # Theaters DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.address}"


class Movies(db.Model):  # Movies DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.gender}"


class Reservations(db.Model):  # Reservations DB
    __table_args__ = (
                         db.UniqueConstraint('reservation', 'theaterID', 'movie_name')),  # Unique to avoid overbooking
    id = db.Column(db.Integer, primary_key=True)
    movieID = db.Column(db.Integer, nullable=False)
    movie_name = db.Column(db.String(), nullable=False)
    theaterID = db.Column(db.Integer, nullable=False)
    reservation = db.Column(db.String(3), nullable=False)
    reservation_number = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"{self.movieID} -{self.movie_name} - {self.theaterID} -  {self.reservation}"
