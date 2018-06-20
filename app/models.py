"""
Data model class declarations
"""
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash

class Users:
    """
    User model class
    """
    def __init__(self, user_details):
        self.user_id = randint(1, 10)
        self.first_name = user_details[0]
        self.last_name = user_details[1]
        self.email = user_details[2]
        self.hashed_password = generate_password_hash(user_details[3])
        self.car_details = None

    def verify_password(self, password):
        """
        Check if password given matches password_hash
        """
        return check_password_hash(self.hashed_password, password)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Rides:
    """
    Rides class declaration
    """
    def __init__(self, origin, destination, date_of_travel, price):
        self.ride_id = randint(1, 10)
        self.origin = origin
        self.destination = destination
        self.travel_date = date_of_travel
        self.price = price
        self.requests = []

    def request(self, request):
        """
        Request the ride method
        """
        self.requests.append(request)

    def __str__(self):
        return '{} to {}'.format(self.origin, self.destination)
