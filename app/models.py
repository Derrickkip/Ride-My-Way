"""
Data model class declarations
"""
from random import randint
from werkzeug.security import generate_password_hash

class Users:
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

class Rides:
    """
    Rides class declaration
    """
    def __init__(self, origin, destination, date, time, price):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.time = time
        self.price = price
