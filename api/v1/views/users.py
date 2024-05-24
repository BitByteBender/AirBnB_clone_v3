#!/usr/bin/python3
""" User-API-Views """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
import json


UPATH = '/users'


@app_views.route(UPATH,
                 methods=['GET'], strict_slashes=False)
def retrieve_users():
    """ Retrieves list of all User objs """
    return (json.dumps([usr.to_dict() for usr in storage.all(User).values()],
            indent=2) + '\n', 200)


@app_views.route(UPATH + '/<user_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """ Retrieves a User obj """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return (json.dumps(user_obj.to_dict(), indent=2) + '\n')


@app_views.route(UPATH + '/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """ Deletes a User obj """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    try:
        storage.delete(user_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"error": str(e)}), 500)


@app_views.route(UPATH,
                 methods=['POST'], strict_slashes=False)
def create_user():
    """ Inserts a User obj """
    dt = request.get_json() or abort(400, "Not a JSON")
    if "email" not in dt:
        abort(400, "Missing email")
    if "password" not in dt:
        abort(400, "Missing password")
    new = User(**dt)
    storage.new(new)
    storage.save()
    return (json.dumps(new.to_dict(), indent=2) + '\n', 201)


@app_views.route(UPATH + '/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a User obj """
    user_obj = storage.get(User, user_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    [setattr(user_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'email', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(user_obj.to_dict(), indent=2) + '\n', 200)
