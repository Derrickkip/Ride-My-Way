"""
tests for user authentication
"""
import pytest
import json

data = [{'first_name':'Simon', 'last_name': 'Mbugua', 
        'email': 'simon@email.com', 'password':"testpassword" },
        {'email':'simon@email.com', 'password':"testpassword"},
        {'email': 'swwee@mail.com', 'password':"testpassword"}
    ]


def test_signup(test_client):
    """
    test that accounts can be created
    """ 
    
    response = test_client.post('/auth/signup', data=json.dumps(data[0]),
                                content_type='application/json')

    assert response.status_code == 201

def test_signup_twice(test_client):
    """
    test that an already signed in user cannot sign in again
    """

    response = test_client.post('/auth/signup', data=json.dumps(data[0]),
                                content_type='application/json')

    assert response.status_code == 400 
    
def test_login(test_client):
    """
    test that user can login into account
    """
    response = test_client.post('/auth/login', data=json.dumps(data[1]),
                                content_type='application/json')

    assert response.status_code == 200

    result = json.loads(response.data)

    assert "access_token" in result.keys()

def test_wrong_credentials(test_client):
    """
    test that it returns 400 error for bad request
    """
    response = test_client.post('/auth/login', data=json.dumps(data[2]),
                                content_type='application/json')

    assert response.status_code == 400

