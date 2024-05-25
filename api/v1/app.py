#!/usr/bin/python3
""" Starts flask app """
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
import json


app = Flask(__name__)
app.register_blueprint(app_views)


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def trigger_error(err):
    """ Triggers a 404 error """
    return (json.dumps({"error": "Not found"}, indent=4) + '\n',
            404, {'Content-Type': 'application/json'})


@app.teardown_appcontext
def teardown_db(exception):
    """ Close storage on teadown """
    storage.close()


if __name__ == "__main__":
    """ Runs flask app on a specified adr and port"""
    host = getenv('HBN_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
