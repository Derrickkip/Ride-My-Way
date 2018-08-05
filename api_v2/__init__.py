
"""
API V2 initialisation
"""
from flask import Flask
from flask_restful import Resource, Api
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import CONFIG
from database.tables import create_tables
from .auth import Signup, Login, User
from .rides import RidesList, Ride, UserRides
from .requests import RideRequests, Respond
from .cars import Car
from .template import TEMPLATE

def create_app(config_name):
    """
    Application Factory
    """

    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    Swagger(app, template=TEMPLATE)
    api = Api(app)

    create_tables(app.config['DATABASE'])

    JWTManager(app)

    CORS(app)

    api.add_resource(Signup, '/api/v2/auth/signup')
    api.add_resource(Login, '/api/v2/auth/login')
    api.add_resource(RidesList, '/api/v2/rides')
    api.add_resource(Ride, '/api/v2/rides/<int:ride_id>')
    api.add_resource(UserRides, '/api/v2/user/rides')
    api.add_resource(RideRequests, '/api/v2/rides/<int:ride_id>/requests')
    api.add_resource(Respond, '/api/v2/rides/<int:ride_id>/requests/<int:request_id>')
    api.add_resource(Car, '/api/v2/cars')
    api.add_resource(User, '/api/v2/users')

    return app
