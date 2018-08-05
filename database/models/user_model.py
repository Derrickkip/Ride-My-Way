"""
User model
Signup and login functionality
"""
import datetime
from flask import abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from .helpers import get_user, get_password, get_user_by_email
from ..dbconn import dbconn

class Users:
    """
    user class definition
    """
    def __init__(self, first_name, last_name, email, phone_number, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password_hash = generate_password_hash(password)

    def signup(self):
        """
        user signup method
        """

        data = [self.first_name, self.last_name, self.email, self.phone_number, self.password_hash]

        if get_user(self.email):
            return {'message': 'user already exists'}, 400

        conn = dbconn()
        cur = conn.cursor()

        sql = """INSERT INTO users (first_name, last_name, email, phone_number, password)
                    VALUES(%s, %s, %s, %s, %s)"""

        cur.execute(sql, data)

        cur.close()

        conn.commit()

        conn.close()

        return {'message': 'user account created'}, 201

    @staticmethod
    def login(email, password):
        """
        login method
        """
        if not get_user(email):
            return {'message': 'The email is not recognised'}, 404

        stored_password = get_password(email)[0]

        if not check_password_hash(stored_password, password):
            return {'message': 'Incorrect password, try again !'}, 400

        expires = datetime.timedelta(days=14)

        access_token = create_access_token(email, expires_delta=expires)

        return {"success":"login successful",
                "access_token": access_token}

    @staticmethod
    def get_user():
        """
        get user details
        """
        email = get_jwt_identity()

        user = get_user_by_email(email)

        user_details = {}

        user_details['first_name']= user[1]
        user_details['last_name'] = user[2]
        user_details['email'] = user[3]
        user_details['phone_number'] = user[4]
        
        return jsonify(user_details)

    @staticmethod
    def update_user(data):
        """
        Update user details
        """
        email = get_jwt_identity()

        user_id = get_user_by_email(email)[0]

        conn = dbconn()
        cur = conn.cursor()

        cur.execute('''update users set first_name=%(first_name)s, last_name=%(last_name)s,
                       phone_number=%(phone_number)s where user_id=%(user_id)s''',
                    {'first_name': data.get('first_name'), 'last_name': data.get('last_name'),
                     'phone_number': data.get('phone_number'), 'user_id': user_id})

        cur.close()
        conn.commit()
        conn.close()

        return {'message': 'Details updated'}