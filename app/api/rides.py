"""
API rides endpoint implementation
"""
from flask import jsonify, abort, request
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


@api.route('/ridemyway/api/v1/rides', methods=['GET', 'POST'])
def get_rides():
    '''
    GET all rides
    '''
    if request.method == 'POST':
        data = request.json

        reqs = ['driver', 'origin', 'destination', 'travel_date', 'time', 'car_model',
                'seats', 'price']
        for req in reqs:
            if not data or not req in data:
                abort(400)

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

@api.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['GET', 'PUT', 'DELETE'])
def get_single_ride(ride_id):
    """
    GET a singe ride
    """
    ride = get_ride_or_abort(ride_id)
    if request.method == 'PUT':
        #check for keys in request data and update key
        for key in request.json.keys():
            ride[key] = request.json.get(key, ride[key])

        return jsonify({'ride':ride})

    elif request.method == 'DELETE':
        RIDES.pop(ride_id)
        return jsonify({}), 204

    return jsonify({'ride': ride})

@api.route('/ridemyway/api/v1/rides/<int:ride_id>/requests', methods=['GET', 'POST'])
def get_requests(ride_id):
    """
    Get requests for ride with ride_id
    """
    ride = get_ride_or_abort(ride_id)
    if request.method == 'POST':
        data = request.json
        requests = ride['requests']
        if requests:
            request_id = requests[-1]['id']+1
        else:
            request_id = 1
        ride_request = {
            'id': request_id,
            'username': data['username']
        }
        requests.append(ride_request)
        return jsonify({'requests': requests}), 201

    requests = ride['requests']
    return jsonify({'requests': requests})
