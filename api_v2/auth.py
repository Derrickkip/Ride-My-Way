"""
Routes for user authentication
"""
import urllib.parse
from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from schema import Schema, And
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

RESULT = urllib.parse.urlparse("postgresql://testuser:testuser@localhost/testdb")
USERNAME = RESULT.username
DATABASE = RESULT.path[1:]
HOSTNAME = RESULT.hostname
PASSWORD = RESULT.password

def get_user(email):
    """
    Helper method to check if user exists in database
    """
    conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                            password=PASSWORD, host=HOSTNAME)

    cur = conn.cursor()

    cur.execute("select * from users where email=%(email)s", {'email':email})

    rows = cur.fetchone()

    return rows is not None

class Signup(Resource):
    """
    Signup route handler
    """
    def __init__(self):
        self.conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                     password=PASSWORD, host=HOSTNAME)

        self.cur = self.conn.cursor()

    def post(self):
        """
        signup for an account
        """
        data = request.json
        schema = Schema({'first_name': And(str, len), 'last_name': And(str, len),
                         'email': And(str, len), 'password': And(str, len)})

        if not schema.is_valid(data):
            return {'error': 'Check your input for missing fields or empty values'}, 400

        for key in data.keys():
            if data[key].isspace():
                return {'error': 'values cannot be empty strings'}, 400

        firstname = data['first_name']
        lastname = data['last_name']
        email = data['email']
        password = data['password']

        password_hash = generate_password_hash(password)

        data = [firstname, lastname, email, password_hash]

        if not get_user(email):

            try:

                sql = """INSERT INTO users (first_name, last_name, email, password)
                            VALUES(%s, %s, %s, %s)"""

                self.cur.execute(sql, data)

                self.cur.close()

                self.conn.commit()

                self.conn.close()

                return {'success': 'user account created'}, 201

            except(Exception, psycopg2.DatabaseError) as error:
                return {'error': str(error)}
        else:
            return {'error': 'user already exists'}, 400


class Login(Resource):
    """
    Login route handler
    """
    def __init__(self):
        self.conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                     password=PASSWORD, host=HOSTNAME)

        self.cur = self.conn.cursor()

    def post(self):
        """
        login into  account
        """
        data = request.json
        schema = Schema({'email': And(str, len), 'password': And(str, len)})

        if not schema.is_valid(data):
            return {'bad request': 'Check your input for missing keys or empty values'}, 400

        for key in data.keys():
            if data[key].isspace():
                return {'error': "values cannot be empty strings"}

        email = data['email']
        password = data['password']

        if get_user(email):
            try:

                self.cur.execute('''SELECT first_name,
                                 password FROM users WHERE email=%(email)s''',
                                 {'email':email})

                rows = self.cur.fetchone()

                if not rows:
                    return {'error': 'Authentication failed user unknown'}

                firstname = rows[0]
                stored_password = rows[1]

                if check_password_hash(stored_password, password):
                    access_token = create_access_token(email, firstname)

                    return {"success":"login successful",
                            "access_token": access_token}

            except(Exception, psycopg2.DatabaseError) as error:
                return jsonify({'error': str(error)})

        return {'error':'wrong credentials'}, 400
