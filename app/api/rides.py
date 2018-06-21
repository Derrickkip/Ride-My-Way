"""
API rides endpoint implementation
"""
from flask import jsonify

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
