
"""
API V2 initialisation
"""
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from config import CONFIG
from .auth import Signup, Login
from .rides import Rides, Ride, CreateRide, MakeRequest, Requests, Respond
from .errors import errors

def create_app(config_name):
    """
    Application Factory
    """

    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    api = Api(app, errors=errors)

    jwt = JWTManager(app)

    api.add_resource(Signup, '/auth/signup')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Rides, '/rides')
    api.add_resource(Ride, '/rides/<int:ride_id>')
    api.add_resource(CreateRide, '/users/rides')
    api.add_resource(MakeRequest, '/rides/<int:ride_id>/requests')
    api.add_resource(Requests, '/users/rides/<int:ride_id>')
    api.add_resource(Respond, '/users/rides/<int:ride_id>/requests/<int:request_id>')

    return app
