#!/usr/bin/python3
""" defines route that returns API status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns API status """
    return (jsonify({"status": "OK"}))
