#!/usr/bin/python3
"""
Reviews API endpoint
"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews(place_id):
    """Obtaining all Reviews of a Place"""
    if storage.get(Place, place_id) is not None:
        place = storage.get(Place, place_id)
        all_reviews = storage.all(Review).values()
        reviews_dict = [review.to_dict() for review in all_reviews]
        match = [review for review in reviews_dict if review['place_id'] == place.id]
        return jsonify(match)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """Obtaining a specific Review"""
    if storage.get(Review, review_id) is not None:
        review = storage.get(Review, review_id)
        return jsonify(review.to_dict()), 200
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deleting a Review"""
    if storage.get(Review, review_id) is not None:
        review = storage.get(Review, review_id)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Creating a Review"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    if 'test' not in request.get_json():
        abort(400., "Missing text")

    if storage.get(Place, place_id) is not None:
        if storage.get(User, request.json['user_id']) is not None:
            new_review = Review(text=request.json['text'], 
                                place_id=place_id,
                                user_id=request.json['user_id'])
            storage.new(new_review)
            storage.save()
            review = new_review.to_dict()
            return jsonify(review), 201
        else:
            abort(404)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def edit_review(review_id):
    """Editing a Review"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if storage.get(Review, review_id) is not None:
        review = storage.get(Review, review_id)
        if 'text' in request.get_json():
            review.text = request.json['text']
        storage.save()
        review = storage.get(Review, review_id)
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
