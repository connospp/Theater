from flask import Blueprint
from main_app.models import Theaters

theaters_bp = Blueprint('theaters', __name__)  # Theaters endpoint reaches here


@theaters_bp.route('/')  # theaters/ will load all theaters with address and name
def get_theaters():
    theaters = Theaters.query.all()
    output = []
    for theater in theaters:
        theater_data = {'name': theater.name, 'address': theater.address}
        output.append(theater_data)

    return {"theaters": output}


@theaters_bp.route('/<id>') # theaters/id will show selected theater with name and addres
def get_theater(id):
    theater = Theaters.query.get_or_404(id)
    return {"name": theater.name, "address": theater.address}
