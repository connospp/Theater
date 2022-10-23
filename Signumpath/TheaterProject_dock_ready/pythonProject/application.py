from main_app.Theaters.theaters import theaters_bp
from main_app.Movies.movies import movies_bp
from main_app.Reservations.reservations import reservations_bp

import config

app = config.app
app.register_blueprint(theaters_bp, url_prefix='/theaters')  # Theaters endpoint send to other module
app.register_blueprint(movies_bp, url_prefix='/movies')  # Movies endpoint send to other module
app.register_blueprint(reservations_bp, url_prefix='/reservations')  # Reservations endpoints send to other module

app.config.from_pyfile('./config.py')  # Attach app from config file


@app.route('/')
def index():  # Landing-page shows following text
    return f'Welcome to Theater Cyprus'
