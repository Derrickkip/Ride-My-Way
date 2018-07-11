
"""
API V2 initialisation
"""
from flask import Flask
from flask_restful import Resource, Api
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import CONFIG
from .auth import Signup, Login
from .rides import Ride, RideRequests, Respond
from .template import TEMPLATE
from database.tables import create_tables

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

    api.add_resource(Signup, '/auth/signup')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Ride, '/rides', '/rides/<int:ride_id>')
    api.add_resource(RideRequests, '/rides/<int:ride_id>/requests')
    api.add_resource(Respond, '/rides/<int:ride_id>/requests/<int:request_id>')

    return app
