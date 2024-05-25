#!/usr/bin/python3
""" Review-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
import json


PPATH = '/places'
RPATH = '/reviews'


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrieve_reviews(place_id):
    """ Retrieves list of all Review objs of a Place """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    return (json.dumps([rv.to_dict() for rv in place_obj.reviews],
            indent=2) + '\n', 200)


@app_views.route(RPATH + '/<review_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_review(review_id):
    """ Retrieves a Review obj """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    return (json.dumps(review_obj.to_dict(), indent=2) + '\n')


@app_views.route(RPATH + '/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """ Deletes a Review obj """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    try:
        storage.delete(review_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"error": str(e)}), 500)


@app_views.route(PPATH + '/<place_id>' + RPATH,
                 methods=['POST'], strict_slashes=False)
def insert_review(place_id):
    """ Inserts a Review obj """
    place_obj = storage.get(Place, place_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    if "user_id" not in dt:
        abort(400, "Missing user_id")
    if "text" not in dt:
        abort(400, "Missing text")
    user_obj = storage.get(User, dt['user_id']) or abort(404)
    dt['place_id'] = place_id
    new = Review(**dt)
    storage.new(new)
    storage.save()
    return (json.dumps(new.to_dict(), indent=2) + '\n', 201)


@app_views.route(RPATH + '/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates Review obj """
    review_obj = storage.get(Review, review_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    [setattr(review_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(review_obj.to_dict(), indent=2) + '\n', 200)
