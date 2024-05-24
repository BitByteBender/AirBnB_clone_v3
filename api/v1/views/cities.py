#!/usr/bin/python3
""" City-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
import json


# dt = request.get_json()
SPATH = '/states'
CPATH = '/cities'


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_cities(state_id):
    """ Retrieves list of all City objs of a State """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    return (json.dumps([c.to_dict() for c in state_obj.cities],
            indent=2) + '\n', 200)


@app_views.route(CPATH + '/<city_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """ Retrieves a City obj """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return (json.dumps(city_obj.to_dict(), indent=2) + '\n')


@app_views.route(CPATH + '/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ Deletes a City obj """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    try:
        storage.delete(city_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"error": str(e)}), 500)


@app_views.route(SPATH + '/<state_id>' + CPATH,
                 methods=['POST'], strict_slashes=False)
def insert_city(state_id):
    """ Inserts a City obj """
    state_obj = storage.get(State, state_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    if "name" not in dt:
        abort(400, "Misssing name")
    dt['state_id'] = state_id
    new = City(**dt)
    storage.new(new)
    storage.save()
    return (json.dumps(new.to_dict(), indent=2) + '\n', 201)


@app_views.route(CPATH + '/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates City obj """
    city_obj = storage.get(City, city_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    [setattr(city_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'state_id', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(city_obj.to_dict(), indent=2) + '\n', 200)
