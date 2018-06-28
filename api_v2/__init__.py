from flask import Flask
from flask_restful import Resource, Api
from .auth import Signup, Login
from .rides import Rides, Ride, CreateRide, MakeRequest, Requests, Respond 
from config import CONFIG

def create_app(config_name):
    """
    Application Factory
    """

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Signup, '/auth/signup')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Rides, '/rides')
    api.add_resource(Ride, '/rides/<int:ride_id>')
    api.add_resource(CreateRide, '/users/rides')
    api.add_resource(MakeRequest, '/rides/<int:ride_id>/requests')
    api.add_resource(Requests, '/users/rides/<int:ride_id>')
    api.add_resource(Respond,'/users/rides/<int:ride_id>/requests/<int:request_id>')

    return app
