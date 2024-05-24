#!/usr/bin/python3
""" defines route that returns API status """
from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns API status """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def retrieve_stats():
    """ retrieves class stats """
    cls_counts = {
             "amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")
            }

    return (json.dumps(cls_counts, indent=2) + '\n')
