"""
Cars endpoint
"""
from flask import request
from flask_restful import Resource
from jsonschema import validate, ValidationError
from flask_jwt_extended import jwt_required
from database.models.car_model import Cars
from .schemas import CAR_SCHEMA

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
