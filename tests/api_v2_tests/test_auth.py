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
