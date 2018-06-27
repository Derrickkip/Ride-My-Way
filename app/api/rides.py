"""
API rides endpoint implementation
"""
from flask import jsonify, abort, request
from schema import Schema, And, Use, Optional, Regex
from app.models import RIDES
from . import api


def get_ride_or_abort(ride_id):
    """
    Get ride with specified id or abort if not found
    """
    ride = RIDES.get(ride_id, None)
    if ride is None:
        abort(404)

    return ride


@api.route('/api/v1/rides', methods=['GET', 'POST'])
def rides_operations():
    '''
    Get a list of rides or create a new ride
    '''
    if request.method == 'POST':
        data = request.json

        schema = Schema({'driver': And(str, len), 'origin': And(str, len),
                         'destination': And(str, len), 'travel_date': And(str, len),
                         'time': And(str, len), 'car_model': And(str, len), 'seats': Use(int),
                         'price': Use(int)})

        if not schema.is_valid(data):
            abort(400)

        for key in data.keys():
            if Regex(r'[a-zA-Z0-9]+').validate(data[key]):
                ride = {
                    'id': len(RIDES)+1,
                    'driver': data['driver'],
                    'origin': data['origin'],
                    'destination': data['destination'],
                    'travel_date': data['travel_date'],
                    'time': data['time'],
                    'car_model': data['car_model'],
                    'seats': data['seats'],
                    'price': data['price'],
                    'requests': []
                }

                RIDES[ride['id']] = ride
                return jsonify({"ride": ride}), 201

    return jsonify({'rides': RIDES})

@api.route('/api/v1/rides/<int:ride_id>', methods=['GET', 'PUT', 'DELETE'])
def single_ride_operation(ride_id):
    """
    Read details of a ride, Update a ride, Delete a ride
    """
    ride = get_ride_or_abort(ride_id)
    if request.method == 'PUT':

        data = request.json

        schema = Schema({Optional('driver'): And(str, len), Optional('origin'): And(str, len),
                         Optional('destination'): And(str, len),
                         Optional('travel_date'): And(str, len), Optional('time'): And(str, len),
                         Optional('car_model'): And(str, len),
                         Optional('seats'): Use(int), Optional('price'): Use(int)})

        if not schema.is_valid(data):
            abort(400)

        for key in request.json.keys():
            ride[key] = request.json.get(key, ride[key])

        return jsonify({'ride':ride})

    elif request.method == 'DELETE':
        RIDES.pop(ride_id)
        return jsonify({}), 204

    return jsonify({'ride': ride})

@api.route('/api/v1/rides/<int:ride_id>/requests', methods=['GET', 'POST'])
def requests_operations(ride_id):
    """
    Read a list of ride requests, Request a ride
    """
    ride = get_ride_or_abort(ride_id)
    if request.method == 'POST':
        data = request.json
        requests = ride['requests']
        if requests:
            request_id = requests[-1]['id']+1
        else:
            request_id = 1

        schema = Schema({'username': And(str, len)})
        if not schema.is_valid(data):
            abort(400)
        ride_request = {
            'id': request_id,
            'username': data['username']
        }
        requests.append(ride_request)
        return jsonify({'requests': requests}), 201

    requests = ride['requests']
    return jsonify({'requests': requests})
