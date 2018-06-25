"""
Tests for users api endpoint
"""
import json


def test_get_users(test_client):
    """
    Fetch all users test
    """
    response = test_client.get('/api/v1/users')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['users']['1']['id'] == 1
    assert result['users']['1']['first_name'] == 'Michael'
    assert result['users']['1']['last_name'] == 'Owen'
    assert result['users']['1']['user_name'] == 'Mike'
    assert result['users']['1']['email'] == 'micowen@mail.com'
    assert result['users']['1']['driver_details']['driving_license'] == 'fdwer2ffew3'
    assert result['users']['1']['driver_details']['car_model'] == 'Mitsubishi Evo 8'
    assert result['users']['1']['driver_details']['plate_number'] == 'KYT 312X'
    assert result['users']['1']['driver_details']['seats'] == 4
    assert result['users']['1']['rides_offered'] == 1
    assert result['users']['1']['rides_requested'] == 0

def test_get_single_user(test_client):
    """
    Fetch single user test
    """
    response = test_client.get('/api/v1/users/2')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['user']['id'] == 2
    assert result['user']['first_name'] == 'Wendy'
    assert result['user']['last_name'] == 'Kim'
    assert result['user']['user_name'] == 'wendesky'
    assert result['user']['email'] == 'wendesky@mail.com'
    assert result['user']['driver_details'] == {}
    assert result['user']['rides_offered'] == 0
    assert result['user']['rides_requested'] == 1

def test_unavailable_user(test_client):
    """
    Raise 404 error for unavailable user
    """
    response = test_client.get('/api/v1/users/4')
    assert response.status_code == 404

def test_create_new_user(test_client):
    """
    Create new user test
    """
    my_data = {"first_name": "John", "last_name": "Snow", "user_name":"stark",
               "email":"jsnow@gmail.com", "driver_details": {}}
    response = test_client.post('/api/v1/users', data=json.dumps(my_data),
                                content_type='application/json')
    assert response.status_code == 201
    result = json.loads(response.data)
    assert result['user']['id'] == 3
    assert result['user']['first_name'] == 'John'
    assert result['user']['last_name'] == 'Snow'
    assert result['user']['user_name'] == 'stark'
    assert result['user']['email'] == 'jsnow@gmail.com'
    assert result['user']['driver_details'] == {}
    assert result['user']['rides_offered'] == 0
    assert result['user']['rides_requested'] == 0

def test_empty_post_request(test_client):
    """
    Test returns 404 if no post data
    """
    response = test_client.post('/api/v1/users',
                                content_type='application/json')
    assert response.status_code == 400


def test_missing_field_in_request(test_client):
    """
    Test raises 400 error if first_name is not in request body
    """
    my_data = {"last_name": "Snow", "user_name":"stark",
               "email":"jsnow@gmail.com", "driver_details": {}}

    response = test_client.post('/api/v1/users', data=json.dumps(my_data),
                                content_type='application/json')
    assert response.status_code == 400

def test_update_user(test_client):
    """
    Update user test
    """
    my_data = {"driver_details": {"driving_license": "2dwheuw213", "car_model": "Land Rover",
                                  "plate_number": "KBE 312X", "seats": 8}}

    response = test_client.put('/api/v1/users/2', data=json.dumps(my_data),
                               content_type='application/json')

    assert response.status_code == 200
    result = json.loads(response.data)

    assert result['user']['driver_details']['driving_license'] == '2dwheuw213'
    assert result['user']['driver_details']['car_model'] == 'Land Rover'
    assert result['user']['driver_details']['plate_number'] == 'KBE 312X'
    assert result['user']['driver_details']['seats'] == 8

def test_update_unavailable_user(test_client):
    """
    Test raise 404 error if ride is not available
    """
    my_data = {"driver_details": {"driving_license": "2dwheuw213", "car_model": "Land Rover",
                                  "plate_number": "KBE 312X", "seats": 8}}

    response = test_client.put('/api/v1/users/6', data=json.dumps(my_data),
                               content_type='application/json')

    assert response.status_code == 404

def test_delete_user(test_client):
    """
    Delete User tests
    """
    response = test_client.delete('/api/v1/users/1')
    assert response.status_code == 204
    response2 = test_client.get('/api/v1/users/1')
    assert response2.status_code == 404

def test_delete_unavailable_user(test_client):
    """
    Returns 404 error if user is not available
    """
    response = test_client.delete('/api/v1/users/6')
    assert response.status_code == 404
