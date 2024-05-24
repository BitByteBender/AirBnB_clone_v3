#!/usr/bin/python3
""" Place-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json


CPATH = '/cities'
PPATH = '/places'


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def retrieve_places(city_id):
    """ Retrieves list of all Place objs of a City """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return (json.dumps([pl.to_dict() for pl in city_obj.places],
            indent=2) + '\n', 200)


@app_views.route(PPATH + '/<place_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """ Retrieves a Place obj """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    return (json.dumps(place_obj.to_dict(), indent=2) + '\n')


@app_views.route(PPATH + '/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place obj """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    try:
        storage.delete(place_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"error": str(e)}), 500)


@app_views.route(CPATH + '/<city_id>' + PPATH,
                 methods=['POST'], strict_slashes=False)
def insert_place(city_id):
    """ Inserts a Place obj """
    city_obj = storage.get(City, city_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    if "user_id" not in dt:
        abort(400, "Missing user_id")
    if "name" not in dt:
        abort(400, "Misssing name")
    dt['city_id'] = city_id
    new = Place(**dt)
    storage.new(new)
    storage.save()
    return (json.dumps(new.to_dict(), indent=2) + '\n', 201)


@app_views.route(PPATH + '/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates Place obj """
    place_obj = storage.get(Place, place_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    [setattr(place_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(place_obj.to_dict(), indent=2) + '\n', 200)
