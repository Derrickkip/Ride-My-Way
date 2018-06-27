"""
API error handlers
"""
from flask import jsonify, make_response

from . import api

@api.errorhandler(400)
def bad_request(error):
    """
    Bad request
    """
    return make_response(jsonify({'error':'Bad Request'}), 400)

@api.errorhandler(404)
def not_found(error):
    """
    Not found
    """
    return make_response(jsonify({'error': 'Not found'}), 404)
