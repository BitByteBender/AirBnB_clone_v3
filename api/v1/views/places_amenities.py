#!/usr/bin/python3
""" Place-Amenity-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
import json


PPATH = '/places'
APATH = '/amenities'


@app_views.route(PPATH + '/<place_id>' + APATH,
                 methods=['GET'], strict_slashes=False)
def retrieve_amn_of_pl(place_id):
    """ Retrieves list of all Amenity objs of a Place """
    place_obj = storage.get(Place, place_id) or abort(404)
    return (json.dumps([am.to_dict() for am in place_obj.amenities],
            indent=2) + '\n', 200)


@app_views.route(PPATH + '/<place_id>' + APATH + '/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_am_from_place(place_id, amenity_id):
    """ Deletes an Amenity obj from a place """
    place_obj = storage.get(Place, place_id) or abort(404)
    amenity_obj = storage.get(Amenity, amenity_id) or abort(404)
    if amenity_obj not in place_obj.amenities:
        abort(404)
    place_obj.amenities.remove(amenity_obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route(PPATH + '/<place_id>' + APATH + '/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_am_to_pl(place_id, amenity_id):
    """ Links an Amenity obj into a place """
    place_obj = storage.get(Place, place_id) or abort(404)
    amenity_obj = storage.get(Amenity, amenity_id) or abort(404)
    if amenity_obj in place_obj.amenities:
        return (json.dumps(amenity_obj.to_dict(), indent=2) + '\n', 200)
    place_obj.amenities.append(amenity_obj)
    storage.save()
    return (json.dumps(amenity_obj.to_dict(), indent=2) + '\n', 201)
