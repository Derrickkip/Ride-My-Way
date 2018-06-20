"""
Application package constructor
"""
from flask import Flask

from config import CONFIG

def create_app(config_name):
    """
    Application Factory
    """
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
