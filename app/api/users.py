"""
REST Users resource endpoint
"""

from flask import jsonify, url_for
from . import api

USERS = [
    {
        "id" : 1,
        'first_name': 'Michael',
        'last_name': 'Owen',
        'user_name': 'Mike',
        'email': 'micowen@mail.com',
        'driver_details' : {
            'driving_license': 'fdwer2ffew3',
            'model' : 'Mitsubishi Evo 8',
            'plate_number': 'KYT 312X',
            'seats': 4,
        },
        'rides_offered' : 1,
        'rides_requested' : 0
    },
     {
         'id': 2,
        'first_name': 'Wendy',
        'last_name': 'Kim',
        'user_name': 'wendesky',
        'email': 'wendesky@mail.com',
        'driver_details' : {},
        'rides_offered' : 0,
        'rides_requested' : 1
    }
]

@api.route('/ridemyway/api/v1/users', methods=['GET'])
def get_all_users():
    """
    GET all users
    """
    return jsonify({'users': USERS})

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
