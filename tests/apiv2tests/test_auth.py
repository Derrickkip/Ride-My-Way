"""
test authentication
"""

import json

def test_create_account(test_client):
    """
    Test user can create account
    """
    my_data = {"first_name": "Simon", "last_name": "Mbugua", "username": "simo",
               "Email": "simo@mail.com", "Password": "simobugua"}
    response = test_client.post('/auth/signup', data = json.dumps(my_data),
                                content_type="application/json")
    assert response.status_code == 201

def test_sign_in(test_client):
    """
    test user can signin
    """
    my_data = {"email": "simo@mail.com", "Password": "simobugua"}
    response = test_client.post('auth/login', data=json.dumps(my_data))
    assert response.status_code == 200

