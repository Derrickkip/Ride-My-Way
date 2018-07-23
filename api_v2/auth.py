"""
Routes for user authentication
"""
import re
from flask import request, abort
from flask_restful import Resource
from jsonschema import validate, ValidationError
from database.models.user_model import Users
from .schemas import SIGNUP_SCHEMA, LOGIN_SCHEMA


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9\.]+@[a-zA-Z0-9\.]+\.[a-zA-Z]*$")

class Signup(Resource):
    """
    Signup route handler
    """
    def post(self):
        """
        Signup
        ---
        tags:
            - Auth

        description: Signup for an account

        parameters:
            - name: User
              in: body
              schema:
                $ref: '#/definitions/UserSignup'

        responses:
            201:
                description: Account created successfully
            400:
                description: Bad request
        """
        data = request.json
        try:
            validate(data, SIGNUP_SCHEMA)

            for key in data.keys():
                if data[key].isspace() or data[key] == '':
                    return {'error': 'values cannot be empty strings'}, 400

            if not re.match(EMAIL_REGEX, data['email']):
                return {'Error': 'Invalid email'}, 400

            if data['password'] != data['confirm_password']:
                abort(400, 'Passwords do not match')

            new_user = Users(data['first_name'], data['last_name'],
                             data['email'], data['phone_number'], data['password'])

            response = new_user.signup()

            return response
        except ValidationError as error:
            return {'error': str(error)}, 400

class Login(Resource):
    """
    Login route handler
    """
    def post(self):
        """
        Login
        ---
        tags:
            - Auth

        description: login into account

        parameters:
            - name: login details
              in: body
              schema:
                $ref: '#/definitions/UserLogin'

        responses:
            200:
                description: login successfull
            400:
                description: Bad request
            404:
                description: Wrong credentials

        """
        data = request.json
        try:
            validate(data, LOGIN_SCHEMA)

            for key in data.keys():
                if data[key].isspace() or data[key] == '':
                    return {'error': "values cannot be empty strings"}, 400

            email = data['email']
            password = data['password']

            response = Users.login(email, password)

            return response
        except ValidationError as error:
            return {'error': str(error)}, 400
