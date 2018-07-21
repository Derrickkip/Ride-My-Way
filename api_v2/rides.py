"""
Implements the rides endpoints
"""
from flask import request
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask_jwt_extended import jwt_required
from database.models.ride_model import Rides
from .schemas import RIDE_SCHEMA


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
