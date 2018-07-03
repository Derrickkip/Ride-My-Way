"""
Routes for user authentication
"""
import urllib.parse
from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from jsonschema import validate
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from database.dbsetup import dbconn

SIGNUP_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"}
    }
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"}
    }
}

def get_user(email):
    """
    Helper method to check if user exists in database
    """
    conn = dbconn()

    cur = conn.cursor()

    cur.execute("select * from users where email=%(email)s", {'email':email})

    rows = cur.fetchone()

    cur.close()

    conn.close()

    return rows is not None

class Signup(Resource):
    """
    Signup route handler
    """
    def __init__(self):
        self.conn = dbconn()

        self.cur = self.conn.cursor()

    def post(self):
        """
        Signup
        ---
        tags:
            - Auth
        parameters:
            - name: User
              in: body
              schema:
                $ref: '#/definitions/UserSignup'
        responses:
            201:
                description: Account created successfully
            400:
                description: Bad request
        """
        data = request.json
        validate(data, SIGNUP_SCHEMA)

        for key in data.keys():
            if data[key].isspace():
                return {'error': 'values cannot be empty strings'}, 400

        firstname = data['first_name']
        lastname = data['last_name']
        email = data['email']
        password = data['password']

        password_hash = generate_password_hash(password)

        data = [firstname, lastname, email, password_hash]

        if get_user(email):
            return {'error': 'user already exists'}, 400

        try:

            sql = """INSERT INTO users (first_name, last_name, email, password)
                        VALUES(%s, %s, %s, %s)"""

            self.cur.execute(sql, data)

            self.cur.close()

            self.conn.commit()

            self.conn.close()

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

        return {'success': 'user account created'}, 201


class Login(Resource):
    """
    Login route handler
    """
    def __init__(self):
        self.conn = dbconn()

        self.cur = self.conn.cursor()

    def post(self):
        """
        Login
        ---
        tags:
            - Auth
        description: login into account
        parameters:
            - name: login details
              in: body
              schema:
                $ref: '#/definitions/UserLogin'
        responses:
            200:
                description: login successfull
            400:
                description: Bad request
            404:
                description: Wrong credentials

        """
        data = request.json
        validate(data, LOGIN_SCHEMA)

        for key in data.keys():
            if data[key].isspace():
                return {'error': "values cannot be empty strings"}, 400

        email = data['email']
        password = data['password']

        if get_user(email):
            try:

                self.cur.execute('''SELECT first_name,
                                    password FROM users WHERE email=%(email)s''',
                                 {'email':email})

            except psycopg2.DatabaseError as error:
                return jsonify({'error': str(error)})

            rows = self.cur.fetchone()

            if not rows:
                return {'error': 'Authentication failed user unknown'}

            firstname = rows[0]
            stored_password = rows[1]

            if check_password_hash(stored_password, password):
                access_token = create_access_token(email, firstname)

                return {"success":"login successful",
                        "access_token": access_token}

        return {'error':'wrong credentials'}, 404
