"""
Routes for user authentication
"""
import urllib.parse
from flask import jsonify
from flask_restful import Resource, reqparse
import psycopg2
from passlib.hash import pbkdf2_sha256

result = urllib.parse.urlparse("postgresql://testuser:testuser@localhost/testdb")
username = result.username
dbpassword = result.password
database = result.path[1:]
hostname = result.hostname


class Signup(Resource):
    def post(self):
        """
        signup for an account
        """
        conn = None
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('first_name', type=str, help="user's firstname")
            parser.add_argument('last_name', type=str, help="user's lastname")
            parser.add_argument('email', type=str, help="user's email")
            parser.add_argument('password', type=str, help="password")
            args = parser.parse_args()

            firstname = args['first_name']
            lastname = args['last_name']
            email = args['email']
            password = args['password']

            hash = pbkdf2_sha256.encrypt(password, rounds=200, salt_size=16)

            data = [firstname, lastname, email, hash]

            sql = """INSERT INTO users (first_name, last_name, email, password)
                        VALUES(%s, %s, %s, %s)"""

            conn = psycopg2.connect(database=database, user=username,
                                    password=dbpassword, host=hostname)

            cur = conn.cursor()

            cur.execute(sql, data)

            cur.close()

            conn.commit()

            return {'success': 'user account created'}, 201
        
        except(Exception , psycopg2.DatabaseError) as Error:
                return jsonify({'error': str(Error)})

        finally:
            if conn is not None:
                conn.close()

        
class Login(Resource):
    def post(self):
        """
        login to your account
        """
        pass
        