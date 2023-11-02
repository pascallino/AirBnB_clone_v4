#!/usr/bin/python3
"""states view to handle all states request API"""
from models import storage
from models.state import State
from flask import Flask, jsonify, abort, request, make_response
from werkzeug.exceptions import NotFound
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """retreive all states of the application """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    eachstate = []
    for s in storage.all(State).values():
        eachstate.append(s.to_dict())
    return jsonify(eachstate)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves a State object: GET /api/v1/states/<state_id>"""
    eachstate = storage.get(State, state_id)
    if eachstate is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        abort(404)
        return response
    else:
        return jsonify(eachstate.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def DELETE_state_by_id(state_id):
    """ Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    eachstate = storage.get(State, state_id)
    if eachstate is None:
        abort(404)
    else:
        storage.delete(eachstate)
        storage.save()
        return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
