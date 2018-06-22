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
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result['users'][1]['firstname'] == 'Michael'
    assert result['users'][1]['lastname'] == 'Owen'
    assert result['users'][1]['username'] == 'Mike'
    assert result['users'][1]['email'] == 'micowen@mail.com'
    assert result['users'][1]['driver_details']['driving_licence'] == 'fdwer2ffew3'
    assert result['users'][1]['driver_details']['model'] == 'Mitsubishi Evo 8'
    assert result['users'][1]['driver_details']['plate_number'] == 'KYT 312X'
    assert result['users'][1]['driver_details']['seats'] == 4
    assert result['users'][1]['rides_offered'] == url_for('ridemyway/api/v1/rides/1')
    assert result['users'][1]['rides_requestes'] == []
    assert result['users'][2]['firstname'] == 'Wendy'
    assert result['users'][2]['lastname'] == 'Kim'
    assert result['users'][2]['username'] == 'wendesky'
    assert result['users'][2]['email'] == 'wendesky@mail.com'
    assert result['users'][2]['driver_deatils'] == {}
    assert result['users'][2]['rides_offered'] == []
    assert result['users'][2]['rides_requested'] == url_for('ridemyway/api/v1/rides/2')


def test_get_single_user(test_client):
    """
    Fetch single user test
    """
    pass

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
