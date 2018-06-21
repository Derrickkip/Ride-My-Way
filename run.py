"""
Application entry point
"""
from flask_script import Manager
from app import create_app

APP = create_app('development')

MANAGER = Manager(APP)

if __name__ == '__main__':
    MANAGER.run()
    