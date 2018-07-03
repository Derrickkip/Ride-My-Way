"""
Tests for rides endpoint
"""
import json

DATA = [{'origin': 'Kisumu', 'destination': 'Kericho',
         'date_of_ride': '20th June 2018', 'time': "10:00 pm", "price":100},
        {'origin':'Siaya', 'date_of_ride': '13th July 2018'}]

def get_headers(test_client):
    """
    get headers for user authentication
    """
    data_signup = {'first_name':'Susan', 'last_name': 'Mbugua',
                   'email': 'sue@email.com', 'password':"testpassword"}

    test_client.post('/auth/signup', data=json.dumps(data_signup),
                     content_type='application/json')

    data_login = {'email': 'sue@email.com', 'password':"testpassword"}

    response = test_client.post('/auth/login', data=json.dumps(data_login),
                                content_type='application/json')

    result = json.loads(response.data)
    headers = result['access_token']
    auth_header = 'Bearer '+headers

    return auth_header

def get_ride_id(test_client):
    """
    Returns id of ride for testing
    """
    auth_header = get_headers(test_client)
    response = test_client.get('/rides', headers={'Authorization':auth_header},
                               content_type='application/json')

    result = json.loads(response.data)

    ride_id = result['rides']["1"]["id"]

    return ride_id


def test_get_rides(test_client):
    """
    test user can create rides
    """
    auth_header = get_headers(test_client)
    response = test_client.get('/rides', headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200

def test_unauthenticated_user(test_client):
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
    response = test_client.post('/rides', headers={'Authorization':auth_header},
                                data=json.dumps(DATA[0]), content_type='application/json')

    assert response.status_code == 201

def test_no_duplicate_ride(test_client):
    """
    Ride duplicates should be rejected
    """
    auth_header = get_headers(test_client)
    response = test_client.post('/rides', headers={'Authorization':auth_header},
                                data=json.dumps(DATA[0]), content_type='application/json')

    assert response.status_code == 400

def test_get_single_ride(test_client):
    """
    test user can view details of single ride
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)
    response = test_client.get('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200

def test_user_can_update_ride(test_client):
    """
    test update endpoint working
    """
    auth_header = get_headers(test_client)
    ride_id = get_ride_id(test_client)
    response = test_client.put('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                               data=json.dumps(DATA[1]), content_type='application/json')

    assert response.status_code == 200

def test_users_can_request_rides(test_client):
    """
    Test that requests to rides can be made
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)

    response = test_client.post('/rides/'+str(ride_id)+'/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    assert response.status_code == 200

def test_no_duplicate_requests(test_client):
    """
    Test that a duplicate request raises a 400 error
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)

    response = test_client.post('/rides/'+str(ride_id)+'/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    assert response.status_code == 400

def test_view_ride_requests(test_client):
    """
    Test that ride owner can view ride requests
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)

    response = test_client.get('/rides/'+str(ride_id)+'/requests',
                               headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200

def test_respond_to_rides(test_client):
    """
    Test that user can either accept or reject ride requests
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)

    req_response = test_client.get('/rides/'+str(ride_id)+'/requests',
                                   headers={'Authorization':auth_header},
                                   content_type='application/json')

    result = json.loads(req_response.data)

    request_id = result["1"]["id"]

    status = {'status': "accepted"}

    response = test_client.put('/rides/'+str(ride_id)+'/requests/'+str(request_id),
                               headers={'Authorization':auth_header},
                               data=json.dumps(status), content_type='application/json')

    assert response.status_code == 200

def test_delete_ride(test_client):
    """
    Test that user can delete ride
    """
    auth_header = get_headers(test_client)
    ride_id = get_ride_id(test_client)
    response = test_client.delete('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                                  content_type='application/json')

    assert response.status_code == 200
    