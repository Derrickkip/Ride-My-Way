"""
User model
Signup and login functionality
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from .helpers import get_user, get_password
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
            return {'error': 'user already exists'}, 400

        conn = dbconn()
        cur = conn.cursor()

        sql = """INSERT INTO users (first_name, last_name, email, phone_number, password)
                    VALUES(%s, %s, %s, %s, %s)"""

        cur.execute(sql, data)

        cur.close()

        conn.commit()

        conn.close()

        return {'success': 'user account created'}, 201

    @staticmethod
    def login(email, password):
        """
        login method
        """
        if get_user(email):

            stored_password = get_password(email)[0]

            if not check_password_hash(stored_password, password):
                return {'error': 'Incorrect password, try again !'}, 400

            access_token = create_access_token(email)

            return {"success":"login successful",
                    "access_token": access_token}


        return {'error':'The email is not recognised'}, 404
