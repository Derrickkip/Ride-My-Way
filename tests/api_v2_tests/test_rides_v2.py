"""
Tests for rides endpoint
"""
import json
import unittest
from api_v2 import create_app

data = [{'origin': 'Kisumu', 'destination': 'Kericho',
         'date_of_ride': '20th June 2018', 'time': "10:00 pm", "price":100}]

def get_headers(test_client):
    """
    get headers for user authentication
    """
    data_signup = {'first_name':'Susan', 'last_name': 'Mbugua', 
                   'email': 'sue@email.com', 'password':"testpassword"}

    test_client.post('/auth/signup', data=json.dumps(data_signup),
                     content_type='application/json')

    data_login = {'email': 'sue@email.com', 'password':"testpassword"}

    response=test_client.post('/auth/login', data=json.dumps(data_login),
                                content_type='application/json')

    result = json.loads(response.data)
    headers = result['access_token']
    auth_header = 'Bearer '+headers

    return auth_header

def test_get_rides(test_client):
    """
    test user can create rides
    """
    auth_header = get_headers(test_client)
    response = test_client.get('/rides', headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200

def test_unauthenticated_user_cant_get_rides(test_client):
    """
    test that user needs auth header to view rides
    """
    response = test_client.get('/rides')

    assert response.status_code == 401

def test_create_ride(test_client):
    """
    test that a user can create rides
    """
    auth_header = get_headers(test_client)  
    response = test_client.post('/users/rides', headers={'Authorization':auth_header},
                                data=json.dumps(data[0]),content_type='application/json')

    assert response.status_code == 201

def test_user_cannot_create_same_ride(test_client):
    """
    Ride duplicates should be rejected
    """
    auth_header = get_headers(test_client)  
    response = test_client.post('/users/rides', headers={'Authorization':auth_header},
                                data=json.dumps(data[0]),content_type='application/json')

    assert response.status_code == 400

