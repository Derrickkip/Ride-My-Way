"""
Test Flask app instance
"""

from flask import current_app

def test_app_created_correctly(test_client):
    '''
    test app created with right configuration
    '''
    assert (current_app is None) is False
    assert (current_app.config['TESTING']) is True
