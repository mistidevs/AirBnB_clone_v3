#!/usr/bin/python3
"""
Places API endpoint
"""
from models import storage
import models
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """Obtaining all Places of a City"""
    if storage.get(City, city_id) is not None:
        city = storage.get(City, city_id)
        all_places = storage.all(City).values()
        places_dict = [place.to_dict() for place in all_places]
        match = [place for place in places_dict if place['city_id'] == city.id]
        return jsonify(match)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Obtaining a specific Place"""
    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deleting a Place"""
    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creating a Place"""
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user id")
    if 'name' not in request.get_json():
        abort(400, "Missing name")

    if storage.get(City, city_id) is not None:
        if storage.get(User, request.json['user_id']) is not None:
            new_place = Place(name=request.json['name'],
                              user_id=request.json['user_id'],
                              city_id=city_id)
            storage.new(new_place)
            storage.save()
            place = new_place.to_dict()
            return jsonify(place), 201
        else:
            abort(404)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"])
def edit_place(place_id):
    """Editing a Place"""
    if not request.is_json:
        abort(400, "Not a JSON")

    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        if 'name' in request.get_json():
            place.name = request.json['name']
        if 'description' in request.get_json():
            place.description = request.json['description']
        if 'number_rooms' in request.get_json():
            place.number_rooms = request.json['number_rooms']
        if 'number_bathrooms' in request.get_json():
            place.number_bathrooms = request.json['number_bathrooms']
        if 'max_guest' in request.get_json():
            place.max_guest = request.json['max_guest']
        if 'price_by_night' in request.get_json():
            place.price_by_night = request.json['price_by_night']
        if 'latitude' in request.get_json():
            place.latitude = request.json['latitude']
        if 'longitude' in request.get_json():
            place.longitude = request.json['longitude']
        if 'amenity_id' in request.get_json() and models.storage_t != 'db':
            place.amenity_ids.append(request.json['amenity_id'])
        storage.save()
        place = storage.get(Place, place_id)
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
