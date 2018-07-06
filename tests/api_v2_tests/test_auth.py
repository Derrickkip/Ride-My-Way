"""
tests for user authentication
"""
import json
import psycopg2
from flask import current_app

DATA = [{'first_name':'Simon', 'last_name': 'Mbugua',
         'email': 'simon@email.com', 'password':"testpassword"},
        {'first_name':'Simon', 'last_name': 'Mbugua',
         'email': 'simonemail.com', 'password':"testpassword"},
        {'email':'simon@email.com', 'password':"testpassword"},
        {'email': 'swwee@mail.com', 'password':"testpassword"}
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

def test_login(test_client):
    """
    test that user can login into account
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[2]),
                                content_type='application/json')

    assert response.status_code == 200

    result = json.loads(response.data)

    assert "access_token" in result.keys()

def test_wrong_credentials(test_client):
    """
    test that it returns 400 error for bad request
    """
    response = test_client.post('/auth/login', data=json.dumps(DATA[3]),
                                content_type='application/json')

    assert response.status_code == 404
