#!/usr/bin/python3
"""
Users API endpoint
"""
from models import storage
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/users/", methods=["GET"])
def get_users():
    users = [user.to_dict() for user in storage.all(User).values()]
    return (jsonify(users)), 200


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if storage.get(User, user_id) is not None:
        user = storage.get(User, user_id)
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if storage.get(User, user_id) is not None:
        user = storage.get(User, user_id)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users/", methods=["POST"])
def create_user():
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'email' not in request.get_json():
        abort(400, "Missing email")
    if 'password' not in request.get_json():
        abort(400, "Missing password")
    new_user = User(email=request.json['email'], 
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    user = new_user.to_dict()
    return jsonify(user), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def edit_user(user_id):
    if not request.get_json():
        abort(400, "Not a JSON")
    if storage.get(User, user_id) is not None:
        user = storage.get(User, user_id)
        if 'first_name' in request.get_json():
            user.first_name = request.json['first_name']
        if 'last_name' in request.get_json():
            user.last_name = request.json['last_name']
        if 'password' in request.get_json():
            user.password = request.json['password']
        storage.save()
        user = storage.get(User, user_id)
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
