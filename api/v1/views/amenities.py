#!/usr/bin/python3
""" State-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
import json


# dt = request.get_json()
APATH = '/amenities'


@app_views.route(APATH,
                 methods=['GET'], strict_slashes=False)
def retrieve_amenities():
    """ Retrieves list of all Amenity objs """
    return (json.dumps([am.to_dict() for am in storage.all(Amenity).values()],
            indent=2) + '\n', 200)


@app_views.route(APATH + '/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_amenity(amenity_id):
    """ Retrieves a Amenity obj """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return (json.dumps(amenity_obj.to_dict(), indent=2) + '\n')


@app_views.route(APATH + '/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """ Deletes an Amenity obj """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    try:
        storage.delete(amenity_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"error": str(e)}), 500)


@app_views.route(APATH,
                 methods=['POST'], strict_slashes=False)
def insert_amenity():
    """ Inserts an Amenity obj """
    dt = request.get_json() or abort(400, "Not a JSON")
    if "name" not in dt:
        abort(400, "Misssing name")
    new = Amenity(**dt)
    storage.new(new)
    storage.save()
    return (json.dumps(new.to_dict(), indent=2) + '\n', 201)


@app_views.route(APATH + '/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ updates Amenity obj """
    amenity_obj = storage.get(Amenity, amenity_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    [setattr(amenity_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(amenity_obj.to_dict(), indent=2) + '\n', 200)
