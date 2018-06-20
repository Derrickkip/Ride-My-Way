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
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Hello World!' in response.data
