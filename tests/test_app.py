"""
Test Flask app instance
"""

from flask import current_app

def test_app_created_correctly(test_client):
    '''
    test app created with right configuration
    '''
    response = test_client.get('ridemyway/api/v1/rides')
    assert response.status_code == 200
    assert (current_app is None) is False
    assert (current_app.config['TESTING']) is True
    assert (current_app.config['DEBUG']) is True
