"""
Requests endpoint
"""
from flask import request
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask_jwt_extended import jwt_required
from database.models.requests_model import Requests
from .schemas import RESPONSE_SCHEMA

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
            - Requests

        security:
            - Bearer: []

        description: Get requests to ride offer

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
            - Requests

        security:
            - Bearer: []

        description: Request to join ride

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
            - Requests
        security:
            - Bearer: []

        description: respond to request

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
        try:
            validate(data, RESPONSE_SCHEMA)

            response = Requests.respond_to_request(ride_id, request_id, data)

            return response

        except ValidationError as error:
            return {'error': str(error)}, 400
