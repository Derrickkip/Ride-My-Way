"""
API rides endpoint implementation
"""
from flask import jsonify, abort, request
from . import api

RIDES = [
    {
        'id': 1,
        'origin': 'Mombasa',
        'destination': 'Nairobi',
        'travel_date': '23th June 2018',
        'time': '10:00 am',
        'price': 500,
        'requests': []
    },
    {
        'id': 2,
        'origin': 'Kisumu',
        'destination': 'Lodwar',
        'travel_date': '25th June 2018',
        'time': '12:00 am',
        'price': 400,
        'requests': []
    }
]

@api.route('/api/v1/rides', methods=['GET'])
def get_rides():
    '''
    GET all rides
    '''
    return jsonify({'rides': RIDES})

@api.route('/api/v1/rides/<int:ride_id>', methods=['GET'])
def get_single_ride(ride_id):
    """
    GET a singe ride
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    return jsonify({'ride': ride[0]})

@api.route('/api/v1/rides', methods=['POST'])
def create_ride():
    """
    Create a ride
    """
    data = request.json
    ride = {
        'id': RIDES[-1]['id']+1,
        'origin': data['origin'],
        'destination': data['destination'],
        'travel_date': data['travel_date'],
        'time': data['time'],
        'price': data['price'],
        'requests': []
    }

    RIDES.append(ride)
    return jsonify({"ride": ride}), 201

@api.route('/api/v1/rides/<int:ride_id>', methods=['PUT'])
def update_ride(ride_id):
    """
    Update ride
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    ride[0]['origin'] = request.json.get('origin', ride[0]['origin'])
    ride[0]['destination'] = request.json.get('destination', ride[0]['destination'])
    ride[0]['travel_date'] = request.json.get('travel_date', ride[0]['travel_date'])
    ride[0]['time'] = request.json.get('time', ride[0]['time'])
    ride[0]['price'] = request.json.get('price', ride[0]['price'])

    return jsonify({'ride':ride[0]})

@api.route('/api/v1/rides/<int:ride_id>', methods=['DELETE'])
def delete_ride(ride_id):
    """
    Delete a ride
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    RIDES.remove(ride[0])
    return jsonify({}), 204
