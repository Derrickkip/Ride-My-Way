"""
REST Users resource endpoint
"""

from flask import jsonify, abort, request
from app.models import USERS
from . import api

def get_user_or_abort(user_id):
    """
    Get user with specified id or abort if not found
    """
    user = [user for user in USERS if user['id'] == user_id]
    if user == []:
        abort(404)

    return user[0]

@api.route('/ridemyway/api/v1/users', methods=['GET', 'POST'])
def users_list():
    """
    Handler for GET and POST requests
    """
    
    if request.method == 'POST':
        data = request.json

        #Check for required fields
        reqs = ['first_name', 'last_name', 'user_name', 'email']
        for req in reqs:
            if data is None or req not in data:
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

    return jsonify({'users': USERS})

@api.route('/ridemyway/api/v1/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def single_user(user_id):
    """
    Handles GET, PUT and DELETE requests
    """
    user = get_user_or_abort(user_id)
    if request.method == 'PUT':
        for key in request.json.keys():
            user[key] = request.json.get(key, user[key])

        return jsonify({'user': user})

    #DELETE request
    elif request.method == 'DELETE':
        USERS.remove(user)
        return jsonify({}), 204

    #GET request
    return jsonify({'user': user})
