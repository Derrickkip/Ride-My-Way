"""
API rides endpoint implementation
"""

from . import api

RIDES = [
    {
        'id': 1,
        'origin': 'Mombasa',
        'Destination': 'Nairobi',
        'Travel_date': '23th June 2018',
        'Price': 500,
        'requests': []
    },
    {
        'id': 2,
        'origin': 'Kisumu',
        'Destination': 'Lodwar',
        'Travel_date': '25th June 2018',
        'Price': 400,
        'requests': []
    }
]

@api.route('/api/v1/rides', methods=['GET'])
def get_rides():
    '''
    GET all rides
    '''
    pass
