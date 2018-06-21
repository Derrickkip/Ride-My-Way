"""
API package constructor
"""
from flask import Blueprint

api = Blueprint('api', __name__)

from . import rides, errors
