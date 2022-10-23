import os
from flask import Blueprint, redirect
from main_app.models import Movies
from main_app.Theaters.theaters import Theaters

movies_bp = Blueprint('movies', __name__)  # movies endpoint reaches here


@movies_bp.route('/')
def get_movies():  # movies/ will load all movies with gender and name
    movies = Movies.query.all()
    output = []
    for movie in movies:
        movie_data = {'name': movie.name, 'gender': movie.gender}
        output.append(movie_data)

    return {"movies": output}


@movies_bp.route('/<id>')
def get_movie(id):  # movies/id will load the selected movie(name and gender) and show all theaters to select from
    movie = Movies.query.get_or_404(id)

    theaters = Theaters.query.all()
    output = []
    for theater in theaters:
        theater_data = {'name': theater.name, 'address': theater.address}
        output.append(theater_data)

    return {"name": movie.name, "gender": movie.gender, "theaters": output}


@movies_bp.route('/<id>/<idt>')
def navigate_booking(id, idt):  # when movie and theater is selected, redirect to reservations endpoint
    URL = os.environ.get("FLASK_RUN_HOST")
    PORT = os.environ.get("FLASK_RUN_PORT")
    return redirect(f'http://{URL}:{PORT}/reservations/{id}/{idt}')
