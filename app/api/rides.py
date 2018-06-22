"""
API rides endpoint implementation
"""
from flask import jsonify, abort, request
from . import api

RIDES = [
    {
        'id': 1,
        'driver': 'Michael Owen',
        'origin': 'Mombasa',
        'destination': 'Nairobi',
        'travel_date': '23th June 2018',
        'time': '10:00 am',
        'car_model': 'Mitsubishi Evo 8',
        'seats': 4,
        'price': 500,
        'requests': []
    },
    {
        'id': 2,
        'driver': 'Sam West',
        'origin': 'Kisumu',
        'destination': 'Lodwar',
        'travel_date': '25th June 2018',
        'time': '12:00 am',
        'car_model':'Subaru Imprezza',
        'seats':3,
        'price': 400,
        'requests': []
    }
]

@api.route('/ridemyway/api/v1/rides', methods=['GET'])
def get_rides():
    '''
    GET all rides
    '''
    return jsonify({'rides': RIDES})

@api.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['GET'])
def get_single_ride(ride_id):
    """
    GET a singe ride
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    return jsonify({'ride': ride[0]})

@api.route('/ridemyway/api/v1/rides', methods=['POST'])
def create_ride():
    """
    Create a ride
    """
    data = request.json
    if data is None:
        abort(400)
    if not 'driver' in data:
        abort(400)
    elif not 'origin' in data:
        abort(400)
    elif not 'destination' in data:
        abort(400)
    elif not 'travel_date' in data:
        abort(400)
    elif not 'time' in data:
        abort(400)
    elif not 'car_model' in data:
        abort(400)
    elif not 'seats' in data:
        abort(400)
    elif not 'price' in data:
        abort(400)
    ride = {
        'id': RIDES[-1]['id']+1,
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

    RIDES.append(ride)
    return jsonify({"ride": ride}), 201

@api.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['PUT'])
def update_ride(ride_id):
    """
    Update ride
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    ride[0]['driver'] = request.json.get('driver', ride[0]['driver'])
    ride[0]['origin'] = request.json.get('origin', ride[0]['origin'])
    ride[0]['destination'] = request.json.get('destination', ride[0]['destination'])
    ride[0]['travel_date'] = request.json.get('travel_date', ride[0]['travel_date'])
    ride[0]['time'] = request.json.get('time', ride[0]['time'])
    ride[0]['car_model'] = request.json.get('car_model', ride[0]['car_model'])
    ride[0]['seats'] = request.json.get('seats', ride[0]['seats'])
    ride[0]['price'] = request.json.get('price', ride[0]['price'])

    return jsonify({'ride':ride[0]})

@api.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['DELETE'])
def delete_ride(ride_id):
    """
    Delete a ride
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    RIDES.remove(ride[0])
    return jsonify({}), 204

@api.route('/ridemyway/api/v1/rides/<int:ride_id>/requests', methods=['GET'])
def get_requests(ride_id):
    """
    Get requests for ride with ride_id
    """
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    requests = ride[0]['requests']
    return jsonify({'requests': requests})

@api.route('/ridemyway/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
def request_ride(ride_id):
    """
    Request ride
    """
    data = request.json
    ride = [ride for ride in RIDES if ride['id'] == ride_id]
    if ride == []:
        abort(404)
    requests = ride[0]['requests']
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
