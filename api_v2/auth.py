"""
Routes for user authentication
"""
import urllib.parse
from flask import jsonify, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

parser = reqparse.RequestParser()

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
    def post(self):
        """
        signup for an account
        """
        conn = None
        parser.add_argument('first_name', type=str, help="user's firstname")
        parser.add_argument('last_name', type=str, help="user's lastname")
        parser.add_argument('email', type=str, help="user's email")
        parser.add_argument('password', type=str, help="password")
        args = parser.parse_args()

        firstname = args['first_name']
        lastname = args['last_name']
        email = args['email']
        password = args['password']

        password_hash = generate_password_hash(password)

        data = [firstname, lastname, email, password_hash]

        if not get_user(email):

            try:

                sql = """INSERT INTO users (first_name, last_name, email, password)
                            VALUES(%s, %s, %s, %s)"""

                conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                        password=PASSWORD, host=HOSTNAME)

                cur = conn.cursor()

                cur.execute(sql, data)

                cur.close()

                conn.commit()

                conn.close()

                return {'success': 'user account created'}, 201

            except(Exception, psycopg2.DatabaseError) as error:
                return {'error': str(error)}
        else:
            return {'error': 'user already exists'}, 400


class Login(Resource):
    """
    Login route handler
    """
    def post(self):
        """
        login into  account
        """
        conn = None
        parser.add_argument('email', type=str, help='users email')
        parser.add_argument('password', type=str, help='password')
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        if get_user(email):
            try:
                conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                        password=PASSWORD, host=HOSTNAME)

                cur = conn.cursor()

                cur.execute("SELECT first_name, password FROM users WHERE email=%(email)s",
                            {'email':email})

                rows = cur.fetchone()

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
