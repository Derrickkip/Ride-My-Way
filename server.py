"""
App entry point
"""

from api_v2 import create_app

APP = create_app('testing')

if __name__ == '__main__':
    APP.run()
    