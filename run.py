"""
Application entry point
"""
from flask_script import Manager
from app import create_app

APP = create_app('development')

port = int(os.environ["PATH"])

MANAGER = Manager(APP)

if __name__ == '__main__':
    MANAGER.run(port=port, host="0.0.0.0")
    