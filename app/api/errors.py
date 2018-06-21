"""
API error handlers
"""
from flask import jsonify, make_response

from . import api

@api.errorhandler(400)
def Bad_request(error):
    """
    Bad request
    """
    return make_response(jsonify({'error':'Bad Request'}), 400)

@api.errorhandler(401)
def unauthorized(error):
    """
    Unauthorized access
    """
    return make_response(jsonify({'error': 'Unauthorized'}))

@api.errorhandler(404)
def not_found(error):
    """
    Not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(500)
def internal_server_error(error):
    """
    Server error
    """
    return make_response(jsonify({'error':'Internal Server error'}))

@api.errorhandler(501)
def not_implemented(error):
    """
    Service not implemented
    """
    return make_response(jsonify({'error':'Not implemented'}))

