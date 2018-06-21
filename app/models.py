"""
Data model class declarations
"""
from random import randint
import json
from werkzeug.security import generate_password_hash, check_password_hash

class Users:
    """
    User model class
    """
    def __init__(self, user_details):
        self.is_driver = False
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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Drivers(Users):
    """
    Driver Class that inherits from user
    """
    def __init__(self, driver_details, car_details):
        super().__init__(driver_details)
        self.is_driver = True
        self.driving_licence = car_details[0]
        self.car_model = car_details[1]
        self.car_registration_number = car_details[2]
        self.seats_available = car_details[3]
        self.ride_offers = []

    def create_ride(self, ride):
        """
        Create ride method for driver
        """
        self.ride_offers.append(ride)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Requests:
    """
    Request class declaration
    """
    def __init__(self, user_name):
        self.user = user_name

    def accept(self):
        """
        Accept request
        """
        return "Request from {} Accepted".format(self.user)

    def reject(self):
        """
        Reject request
        """
        return "Request from {} Rejected".format(self.user)

    def __str__(self):
        return '<Request: {}>'.format(self.user)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
