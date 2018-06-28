"""
tests for user authentication
"""

import json

def test_signup(test_client):
    """
    test that accounts can be created
    """
    my_data = {'first_name':'Simon', 'last_name': 'Mbugua', 
               'email': 'test@email.com', 'password':"testpassword" }
    
    response = test_client.post('/auth/signup', data=json.dumps(my_data),
                                content_type='application/json')

    assert response.status_code == 201

def test_login(test_client):
    """
    test that user can login into account
    """
    my_data = {'email':'test@mail.com', 'password':"testpassword"}
    response = test_client.post('/auth/login', data=json.dumps(my_data),
                                content_type='application/json')

    assert response.status_code == 200

    result = json.loads(response.data)

    assert "access_token" in result.keys()
