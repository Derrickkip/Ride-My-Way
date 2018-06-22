"""
REST Users resource endpoint
"""

from flask import jsonify, abort, request
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
            'car_model' : 'Mitsubishi Evo 8',
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
    user = [user for user in USERS if user['id'] == user_id]
    if user == []:
        abort(404)
    return jsonify({'user': user[0]})

@api.route('/ridemyway/api/v1/users', methods=['POST'])
def create_user():
    """
    Create new user
    """
    data = request.json
    if data is None:
        abort(400)
    elif not 'first_name' in data:
        abort(400)
    elif not 'last_name' in data:
        abort(400)
    elif not 'user_name' in data:
        abort(400)
    elif not 'email' in data:
        abort(400)
    
    user = {
        'id': USERS[-1]['id']+1,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'user_name': data['user_name'],
        'email': data['email'],
        'driver_details' : data.get('driver_details', {}),
        'rides_offered' : 0,
        'rides_requested' : 0
    }

    USERS.append(user)

    return jsonify({'user': user}), 201

@api.route('/ridemyway/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user
    """
    user = [user for user in USERS if user['id'] == user_id]
    if user == []:
        abort(404)
    user[0]['first_name']= request.json.get('first_name', user[0]['first_name'])
    user[0]['last_name']= request.json.get('last_name', user[0]['last_name'])
    user[0]['user_name']= request.json.get('user_name', user[0]['user_name'])
    user[0]['email']= request.json.get('email', user[0]['email'])
    user[0]['driver_details']= request.json.get('driver_details', user[0]['driver_details'])

    return jsonify({'user': user[0]})     

@api.route('/ridemyway/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete user
    """
    pass
