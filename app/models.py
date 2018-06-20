"""
Data model class declarations
"""
from random import randint
from werkzeug.security import generate_password_hash

class User:
    """
    User model class
    """
    def __init__(self, first_name, last_name, email, password):
        self.user_id = randint(1, 10)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = generate_password_hash(password)
        self.car_details = None

class Driver(User):
    """
    Driver model class inherits User
    """
    pass

class Rides:
    """
    Rides class declaration
    """
    pass
