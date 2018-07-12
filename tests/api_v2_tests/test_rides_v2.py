"""
Tests for rides endpoint
"""
import json
import psycopg2
from flask import current_app

DATA = [{'origin': 'Kisumu', 'destination': 'Kericho',
         'date_of_ride': '20th June 2018', 'time': "10:00 pm", "price":100},
        {'origin':'Siaya', 'date_of_ride': '13th July 2018'},
        {'origin': 'CBD', 'destination': 'Westlands',
         'date_of_ride': '5th Sep 2018', 'time':'11:00am', "price": 300}]

def dbconn():
    """
    database connection for the test
    """
    dbase = current_app.config['DATABASE']

    conn = psycopg2.connect(dbase)

    return conn

def get_rides_in_db():
    """
    return the number of users in the db
    """
    conn = dbconn()

    cur = conn.cursor()

    cur.execute('select * from rides')

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return len(rows)

def get_ride(ride_id):
    """
    returns the details of the ride with the given id
    """
    conn = dbconn()

    cur = conn.cursor()

    cur.execute('''select
                origin,
                date_of_ride 
                from rides where ride_id=%(ride_id)s''',
                {'ride_id': ride_id})

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row

def get_requests():
    """
    returns the number of requests in the db
    """
    conn = dbconn()

    cur = conn.cursor()

    cur.execute('select * from requests')

    rows = cur.fetchall()

    return len(rows)


def get_headers(test_client):
    """
    get headers for user authentication
    """
    ############### USER 1 ########################

    user1 = {'first_name':'Susan', 'last_name': 'Mbugua',
             'email': 'sue@email.com', 'password':"testpassword"}

    test_client.post('/auth/signup', data=json.dumps(user1),
                     content_type='application/json')

    data_login = {'email': 'sue@email.com', 'password':"testpassword"}

    response1 = test_client.post('/auth/login', data=json.dumps(data_login),
                                 content_type='application/json')

    result = json.loads(response1.data)
    headers = result['access_token']
    auth_header1 = 'Bearer '+headers

    ############## USER 2 ###############################

    user2 = {'first_name':'Luke', 'last_name': 'Skywalker',
             'email': 'skywalker@email.com', 'password':"testpassword"}

    test_client.post('/auth/signup', data=json.dumps(user2),
                     content_type='application/json')

    data_login2 = {'email': 'skywalker@email.com', 'password':"testpassword"}

    response2 = test_client.post('/auth/login', data=json.dumps(data_login2),
                                 content_type='application/json')

    result2 = json.loads(response2.data)
    headers2 = result2['access_token']
    auth_header2 = 'Bearer '+headers2

    auth_headers = [auth_header1, auth_header2]

    return auth_headers

def get_ride_id(test_client):
    """
    Returns id of a ride for testing
    """
    auth_header = get_headers(test_client)[0]
    response = test_client.get('/rides', headers={'Authorization':auth_header},
                               content_type='application/json')

    result = json.loads(response.data)

    ride_id = result['rides']["1"]["id"]

    return ride_id


def test_get_rides(test_client):
    """
    test user can create rides
    """
    auth_header = get_headers(test_client)[0]
    response = test_client.get('/rides', headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200

    result = json.loads(response.data)

    assert 'message' in result

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
    initial_count = get_rides_in_db()
    auth_header = get_headers(test_client)[0]
    response = test_client.post('/rides', headers={'Authorization':auth_header},
                                data=json.dumps(DATA[0]), content_type='application/json')

    assert response.status_code == 201
    final_count = get_rides_in_db()
    assert final_count - initial_count == 1


def test_no_duplicate_ride(test_client):
    """
    Ride duplicates should be rejected
    """
    auth_header = get_headers(test_client)[0]
    response = test_client.post('/rides', headers={'Authorization':auth_header},
                                data=json.dumps(DATA[0]), content_type='application/json')

    assert response.status_code == 400

    response2 = test_client.post('/rides', headers={'Authorization':auth_header},
                                data=json.dumps(DATA[2]), content_type='application/json')

    assert response2.status_code == 201

    response3 = test_client.post('/rides', headers={'Authorization':auth_header},
                                data=json.dumps(DATA[2]), content_type='application/json')

    assert response3.status_code == 400

def test_get_single_ride(test_client):
    """
    test user can view details of single ride
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[0]
    response = test_client.get('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200


def test_non_existent_ride(test_client):
    """
    test that requesting for none existent ride raises 404 error
    """
    auth_header = get_headers(test_client)[0]
    response = test_client.get('/rides/50000', headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 404

def test_user_can_update_ride(test_client):
    """
    test update endpoint working
    """
    auth_header = get_headers(test_client)[0]
    ride_id = get_ride_id(test_client)
    response = test_client.put('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                               data=json.dumps(DATA[1]), content_type='application/json')

    assert response.status_code == 200

    ride = get_ride(ride_id)

    #check value in origin is updated
    assert ride[0] == 'Siaya'
    #Check value in date_of_ride is updated
    assert ride[1] == '13th July 2018'

def test_update_non_existent_ride(test_client):
    """
    test raises 404 error
    """
    auth_header = get_headers(test_client)[0]
    response = test_client.put('/rides/50000', headers={'Authorization':auth_header},
                               data=json.dumps(DATA[1]), content_type='application/json')

    assert response.status_code == 404



def test_users_can_request_rides(test_client):
    """
    Test that requests to rides can be made
    """
    initial_count = get_requests()
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[1]

    response = test_client.post('/rides/'+str(ride_id)+'/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    assert response.status_code == 200

    final_count = get_requests()

    assert final_count - initial_count == 1

def test_no_duplicate_requests(test_client):
    """
    Test that a duplicate request raises a 400 error
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[1]

    response = test_client.post('/rides/'+str(ride_id)+'/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    assert response.status_code == 400

def test_owner_cannot_request_ride(test_client):
    """
    Ride owner should not be able to request his ride
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[0]
    response = test_client.post('/rides/'+str(ride_id)+'/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    assert response.status_code == 400


def test_request_non_existent_ride(test_client):
    """
    Test returns 404 if ride is not availabe
    """
    auth_header = get_headers(test_client)[0]

    response = test_client.post('/rides/5000/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    assert response.status_code == 404

def test_view_ride_requests(test_client):
    """
    Test that ride owner can view ride requests
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[0]

    response = test_client.get('/rides/'+str(ride_id)+'/requests',
                               headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 200

def test_only_owner_view_requests(test_client):
    """
    Only ride owner should view ride
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[1]

    response = test_client.get('/rides/'+str(ride_id)+'/requests',
                               headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 403

def test_requests_of_missing_ride(test_client):
    """
    Should return 404 if ride not found
    """
    auth_header = get_headers(test_client)[0]

    response = test_client.get('/rides/5000/requests',
                               headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 404

def test_respond_to_rides(test_client):
    """
    Test that user can either accept or reject ride requests
    """
    ride_id = get_ride_id(test_client)
    auth_header = get_headers(test_client)[0]

    req_response = test_client.get('/rides/'+str(ride_id)+'/requests',
                                   headers={'Authorization':auth_header},
                                   content_type='application/json')

    result1 = json.loads(req_response.data)

    request_id = result1["1"]["id"]

    status = {'status': "accepted"}

    response = test_client.put('/rides/'+str(ride_id)+'/requests/'+str(request_id),
                               headers={'Authorization':auth_header},
                               data=json.dumps(status), content_type='application/json')

    assert response.status_code == 200

    #Check that request is updated
    response2 = test_client.get('/rides/'+str(ride_id)+'/requests',
                                headers={'Authorization':auth_header},
                                content_type='application/json')

    result = json.loads(response2.data)

    assert result['1']['accept_status'] == "accepted"

def test_delete_ride(test_client):
    """
    Test that user can delete ride
    """
    initial_count = get_rides_in_db()
    auth_header = get_headers(test_client)[0]
    ride_id = get_ride_id(test_client)
    response = test_client.delete('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                                  content_type='application/json')

    assert response.status_code == 200

    final_count = get_rides_in_db()

    assert initial_count - final_count == 1

    #check that ride does not exist
    response = test_client.get('/rides/'+str(ride_id), headers={'Authorization':auth_header},
                               content_type='application/json')

    assert response.status_code == 404
   