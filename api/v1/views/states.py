#!/usr/bin/python3
""" State-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
import json


# dt = request.get_json()
PATH = '/states/'


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    """ Retrieves list of all State objs """
    state_recs = storage.all(State).values()
    return (json.dumps([s.to_dict() for s in state_recs], indent=2) + '\n')


@app_views.route(PATH + '<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state(state_id):
    """ Retrieves a State obj """
    return (json.dumps(storage.get(State, state_id).to_dict(), indent=2)
            + '\n' if storage.get(State, state_id) else abort(404))


@app_views.route(PATH + '<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """ Deletes a state obj """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    try:
        storage.delete(state_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"error": str(e)}), 500)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def insert_state():
    """ Inserts a new State """
    dt = request.get_json()
    if not isinstance(dt, dict) or "name" not in dt:
        abort(400, "Not JSON" if not isinstance(dt, dict)
              else "Misssing name")
    new = State(**dt)
    storage.new(new)
    storage.save()
    return (json.dumps(new_state.to_dict()) + '\n', 201)


@app_views.route(PATH + '<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates State obj """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    dt = request.get_json()
    [setattr(state_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(state_obj.to_dict(), indent=2) + '\n', 200)
