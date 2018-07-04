"""
Implements the rides endpoints
"""
from flask import request
from flask_restful import Resource
from jsonschema import validate
from flask_jwt_extended import jwt_required
from database.dbsetup import Rides, Requests

RIDE_SCHEMA = {
    "type": "object",
    "properties": {
        "origin": {"type": "string"},
        "destination": {"type": "string"},
        "date_of_ride": {"type": "string"},
        "time": {"type": "string"},
        "price": {"type": "number"}
    }
}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"enum": ["accepted", "rejected"]}
    }
}


class RidesEndpoint(Resource):
    """
    handler for /rides endpoint
    """
    @jwt_required
    def get(self):
        """
        get all ride offers
        ---
        tags:
            - Rides
        security:
            - Bearer: []
        responses:
            200:
                description: Success
                schema:
                    $ref: '#/definitions/Rides'

        """

        response = Rides.get_all_rides()

        return response

    @jwt_required
    def post(self):
        """
        create a new ride offer
        ---
        tags:
            - Rides
        security:
            - Bearer: []
        parameters:
            - name: Rides
              in: body
              schema:
                $ref: '#/definitions/Rides'
        responses:
            201:
                description: Ride successfully created
            400:
                description: Bad request

        """
        data = request.json
        validate(data, RIDE_SCHEMA)

        for key in data.keys():
            if str(data[key]).isspace():
                return {'bad request': 'values cannot be spaces'}, 400

        new_ride = Rides(data['origin'], data['destination'],
                         data['date_of_ride'], data['time'], data['price'])

        result = new_ride.create_ride()

        return result


class Ride(Resource):
    """
    Single ride operations
    """
    @jwt_required
    def get(self, ride_id):
        """
        view details of a ride offer
        ---
        tags:
            - Rides
        description: view details of a ride
        security:
            - Bearer: []
        parameters:
            - name: ride_id
              in: path
              type: int
              description: Id of ride to fetch

        responses:
            200:
                description: ride fetched
                schema:
                    $ref: '#/definitions/Rides'
            404:
                description: ride not found

        """
        response = Rides.get_single_ride(ride_id)

        return response

    @jwt_required
    def put(self, ride_id):
        """
        Update ride offer
        ---
        tags:
            - Rides
        description: Update details of a ride send only fields to update
        security:
            - Bearer: []
        parameters:
            - name: ride_id
              in: path
              type: int
              description: Id of ride to update
            - name: ride
              in: body
              schema:
                $ref: '#/definitions/Rides'

        responses:
            200:
                description: ride updated
            404:
                description: ride not found
        """
        data = request.json

        response = Rides.update_ride(ride_id, data)

        return response

    @jwt_required
    def delete(self, ride_id):
        """
        delete ride offer
        ---
        tags:
            - Rides
        security:
            - Bearer: []
        parameters:
            - name: ride_id
              in: path
              type: int
              description: Id of ride to delete
        responses:
            200:
                description: ride deleted
            404:
                description: ride not found

        """
        response = Rides.delete_ride(ride_id)

        return response

class RideRequests(Resource):
    """
    Requests operations
    """
    @jwt_required
    def get(self, ride_id):
        """
        get all requests to a ride offer
        ---
        tags:
            - Rides
        security:
            - Bearer: []

        parameters:
            - name: ride_id
              in: path
              type: int
              description: Id of ride you want to see requests

        responses:
            200:
                description: success
                schema:
                    $ref: '#/definitions/Requests'
            404:
                description: ride not found
        """

        response = Requests.get_all_requests(ride_id)

        return response

    @jwt_required
    def post(self, ride_id):
        """
        request to join a ride offer
        ---
        tags:
            - Rides
        security:
            - Bearer: []

        parameters:
            - name: ride_id
              in: path
              type: int
              description: Id of ride you want requests

        responses:
            200:
                description: successfully requested
            400:
                description: bad request
            404:
                description: ride not found
        """
        response = Requests.make_request(ride_id)

        return response

class Respond(Resource):
    '''
    User should be able to accept or reject a request for ride
    '''
    @jwt_required
    def put(self, ride_id, request_id):
        """
        accept or reject a request to a ride offer
        ---
        tags:
            - Rides
        security:
            - Bearer: []

        parameters:
            - name: ride_id
              in: path
              type: int
              description: Id of ride you want to respond to
            - name: request_id
              in: path
              type: int
              description: Id of request you want to respond to
            - name: response
              in: body
              schema:
                $ref: '#/definitions/Response'

        responses:
            200:
                description: success
            400:
                description: Bad request
            403:
                description: Unauthorised, Only owners of ride can respond to requests
        """
        data = request.json
        validate(data, RESPONSE_SCHEMA)

        response = Requests.respond_to_request(ride_id, request_id, data)

        return response
