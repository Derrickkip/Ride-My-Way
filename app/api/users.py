"""
REST Users resource endpoint
"""

from flask import jsonify, url_for
from . import api

USERS = {
    1 : {
        'first_name': 'Michael',
        'lastname': 'Owen',
        'username': 'Mike',
        'email': 'micowen@mail.com',
        'driver_details' : {
            'driving_license': 'fdwer2ffew3',
            'model' : 'Mitsubishi Evo 8',
            'plate_number': 'KYT 312X',
            'Seats': 4,
        },
        'rides_offered' : [url_for('ridemyway/api/v1/rides/1')],
        'rides_requested' : []
    },
    2 : {
        'first_name': 'Wendy',
        'lastname': 'Kim',
        'username': 'Wendesky',
        'email': 'wendesky@mail.com',
        'driver_details' : {},
        'rides_offered' : [],
        'rides_requested' : [url_for('ridemyway/api/v1/rides/2')]
    }
}

@api.route('/ridemyway/api/v1/users', methods=['GET'])
def get_all_users():
    """
    GET all users
    """
    pass

@api.route('/ridemyway/api/v1/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    """
    GET a single user
    """
    pass

@api.route('/ridemyway/api/v1/users', methods=['POST'])
def create_user():
    """
    Create new user
    """
    pass

@api.route('/ridemyway/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user
    """
    pass

@api.route('/ridemyway/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user
    """
    pass
    