"""
Implements the rides endpoints
"""
from flask import request
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask_jwt_extended import jwt_required
from database.models import Rides, Requests, Cars
from .schemas import RIDE_SCHEMA, RESPONSE_SCHEMA, CAR_SCHEMA


class RidesList(Resource):
    """
    Ride operations
    """
    def get(self):
        """
        view all ride offers
        ---
        tags:
            - Rides

        description: Fetch all ride offers

        responses:
            200:
                description: ride fetched
                schema:
                    $ref: '#/definitions/Ride_details'

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

        description: Create a new ride offer

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
        try:
            validate(data, RIDE_SCHEMA)

            for key in data.keys():
                if str(data[key]).isspace() or data[key] == '':
                    return {'bad request': 'values cannot be spaces'}, 400

            new_ride = Rides(data['origin'], data['destination'],
                             data['date_of_ride'], data['time'], data['price'])

            result = new_ride.create_ride()

            return result

        except ValidationError as error:
            return {'error': str(error)}, 400

class Ride(Resource):
    """
    single ride operations
    """
    @jwt_required
    def get(self, ride_id):
        '''
        get single ride
        ---
        tags:
            - Rides

        description: Fetch single ride offer

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
                    $ref: '#/definitions/Ride_details'
            404:
                description: ride not found

        '''
        response = Rides.get_single_ride(ride_id)

        return response

    @jwt_required
    def put(self, ride_id):
        """
        Update ride offer
        ---
        tags:
            - Rides

        description: Update details of a ride offer

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

        description: Delete ride offer

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

class Car(Resource):
    '''
    Car resource routes
    '''
    @jwt_required
    def post(self):
        """
        Add user's car
        ---
        tags:
            - Cars

        security:
            - Bearer: []

        description: Add car details

        parameters:
            - name: cars
              in: body
              schema:
                $ref: '#/definitions/Cars'

        responses:
            201:
                description: Car details updated
            400:
                description: Bad request
        """
        data = request.json
        try:
            validate(data, CAR_SCHEMA)
            new_car = Cars(data['car_model'], data['registration'], data['seats'])
            response = new_car.create_car()

            return response

        except ValidationError as error:
            return {'error': str(error)}, 400

    @jwt_required
    def get(self):
        """
        Get user's car
        ---
        tags:
            - Cars

        security:
            - Bearer: []

        description: View car details, User can only view their car details

        responses:
            200:
                description: Success
                schema:
                    $ref: '#/definitions/Cars'
            404:
                description: Not found
        """
        response = Cars.get_car()

        return response

    @jwt_required
    def put(self):
        """
        Update car details
        ---
        tags:
            - Cars

        security:
            - Bearer: []

        description: Update car details

        parameters:
            - name: car
              in: body
              schema:
                $ref: '#/definitions/Cars'

        responses:
            200:
                description: successfully updated
        """
        data = request.json
        try:
            validate(data, CAR_SCHEMA)

            response = Cars.update_details(data)

            return response

        except ValidationError as error:
            return {'error': str(error)}, 400

    @jwt_required
    def delete(self):
        '''
        delete car details
        ---
        tags:
            - Cars

        security:
            - Bearer: []

        description: Delete car details

        responses:
            200:
                description: successfully deleted
            404:
                description: no car details
        '''
        response = Cars.delete()

        return response
