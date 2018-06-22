"""
Tests for users api endpoint
"""
import json

from flask import url_for

def test_get_users(test_client):
    """
    Fetch all users test
    """
    response = test_client.get('/ridemyway/api/v1/users')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['users'][0]['first_name'] == 'Michael'
    assert result['users'][0]['last_name'] == 'Owen'
    assert result['users'][0]['user_name'] == 'Mike'
    assert result['users'][0]['email'] == 'micowen@mail.com'
    assert result['users'][0]['driver_details']['driving_license'] == 'fdwer2ffew3'
    assert result['users'][0]['driver_details']['model'] == 'Mitsubishi Evo 8'
    assert result['users'][0]['driver_details']['plate_number'] == 'KYT 312X'
    assert result['users'][0]['driver_details']['seats'] == 4
    assert result['users'][0]['rides_offered'] == 1
    assert result['users'][0]['rides_requested'] == 0
    assert result['users'][1]['first_name'] == 'Wendy'
    assert result['users'][1]['last_name'] == 'Kim'
    assert result['users'][1]['user_name'] == 'wendesky'
    assert result['users'][1]['email'] == 'wendesky@mail.com'
    assert result['users'][1]['driver_details'] == {}
    assert result['users'][1]['rides_offered'] == 0
    assert result['users'][1]['rides_requested'] == 1


def test_get_single_user(test_client):
    """
    Fetch single user test
    """
    response = test_client.get('/ridemyway/api/v1/users/2')
    assert response.status_code == 200
    result = json.loads(response.data)
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
    response = test_client.get('/ridemyway/api/v1/users/4')
    assert response.status_code == 404

def test_create_new_user(test_client):
    """
    Create new user test
    """
    pass

def test_update_user(test_client):
    """
    Update user test
    """
    pass

def test_delete_user(test_client):
    """
    Delete User tests
    """
