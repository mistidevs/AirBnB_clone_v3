#!/usr/bin/python3
"""
Cities API endpoint
"""
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    if storage.get(State, state_id) is not None:
        state = storage.get(State, state_id)
        all_cities = storage.all(City).values()
        cities_dict = [city.to_dict() for city in all_cities]
        cities_list = [city for city in all_cities if city['state_id'] == state.id]
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    if storage.get(City, city_id) is not None:
        city = storage.get(City, city_id)
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    if storage.get(City, city_id) is not None:
        city = storage.get(City, city_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    
    if storage.get(State, state_id) is not None:
        new_city = City(name=request.json['name'], state_id=state_id)
        storage.new(new_city)
        storage.save()
        city = new_city.to_dict()
        return jsonify(city), 201
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def edit_city(city_id):
    if not request.get_json():
        abort(400, "Not a JSON")
    
    if storage.get(City, city_id) is not None:
        city = storage.get(City, city_id)
        city.name = request.json['name']
        storage.save()
        city = storage.get(City,city_id)
        return jsonify(city.to_dict())
    else:
        abort(404)
