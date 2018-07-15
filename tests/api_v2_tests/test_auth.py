"""
tests for user authentication
"""
import json
import psycopg2
from flask import current_app

DATA = [{'first_name':'Simon', 'last_name': 'Mbugua',
         'email': 'simon@email.com', 'phone_number': '+254727138659', 'password':"testpassword"},
        {'first_name':'Simon', 'last_name': 'Mbugua',
         'email': 'simonemail.com', 'phone_number': '+254727138659', 'password':"testpassword"},
        {'first_name':'Simon', 'last_name': 'Mbugua',
         'email': ' ', 'phone_number': '+254727138659', 'password':"testpassword"},
        {'first_name':'Simon', 'email': 'simo@mgugua.com',
         'phone_number': '+254727138659', 'password':"testpassword"},
        {'email':'simon@email.com', 'password':"testpassword"},
        {'email': 'swwee@mail.com', 'password':"testpassword"},
        {'email': 'simon@email.com', 'password': 'testp'},
        {'email': 'simon@email.com', 'password': ' '},
        {'email': 'simon@email.com'}
       ]

def get_users_in_db():
    """
    return the number of users in the db
    """
    dbase = current_app.config['DATABASE']

    conn = psycopg2.connect(dbase)

    cur = conn.cursor()

    cur.execute('select * from users')

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return len(rows)


def test_signup(test_client):
    """
    test that accounts can be created
    """
    initial_count = get_users_in_db()
    response = test_client.post('/auth/signup', data=json.dumps(DATA[0]),
                                content_type='application/json')

    assert response.status_code == 201
    final_count = get_users_in_db()
    assert final_count - initial_count == 1

def test_signup_twice(test_client):
    """
    test that an already signed in user cannot sign in again
    """

    response = test_client.post('/auth/signup', data=json.dumps(DATA[0]),
                                content_type='application/json')

    assert response.status_code == 400

def test_signup_wrong_email(test_client):
    """
    test that a validation error is raised
    """
    response = test_client.post('/auth/signup', data=json.dumps(DATA[1]),
                                content_type='application/json')
    assert response.status_code == 400

def test_signup_empty_string(test_client):
    """
    Should return 400
    """
    response = test_client.post('/auth/signup', data=json.dumps(DATA[2]),
                                content_type='application/json')
    assert response.status_code == 400

def test_signup_missing_field(test_client):
    """
    test returns 400 error
    """
    response = test_client.post('/auth/signup', data=json.dumps(DATA[3]),
                                content_type='application/json')
    assert response.status_code == 400

def test_login(test_client):
    """
    test that user can login into account
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[4]),
                                content_type='application/json')

    assert response.status_code == 200

    result = json.loads(response.data)

    assert "access_token" in result.keys()

def test_wrong_email(test_client):
    """
    test that it returns 404 error for wrong email
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[5]),
                                content_type='application/json')

    assert response.status_code == 404

def test_wrong_password(test_client):
    """
    test returns 400 error for wrong password
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[6]),
                                content_type='application/json')

    assert response.status_code == 400

def test_login_empty_string(test_client):
    """
    test returns 400 for empty strings
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[7]),
                                content_type='application/json')

    assert response.status_code == 400

def test_login_missing_field(test_client):
    """
    test returns 400 error for missing fields
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[8]),
                                content_type='application/json')

    assert response.status_code == 400
