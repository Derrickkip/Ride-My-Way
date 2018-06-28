"""
Implements the rides endpoints
"""
from flask_restful import Resource

class Rides(Resource):
    def get(self):
        """
        fetch all rides
        """
        pass


class Ride(Resource):
    def get(self, ride_id):
        """
        fetch single ride
        """
        pass

class CreateRide(Resource):
    def post(self):
        """
        create a new ride
        """
        pass

class MakeRequest(Resource):
    def post(self, ride_id):
        """
        request a ride
        """
        pass

class Requests(Resource):
    def get(self, ride_id):
        """
        get all requests to ride
        """
        pass

class Respond(Resource):
    def put(self, ride_id, request_id):
        """
        accept or reject a ride
        """
        pass


