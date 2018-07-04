"""
Routes for user authentication
"""
from flask import request
from flask_restful import Resource
from jsonschema import validate
from database.dbsetup import Users

SIGNUP_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"}
    }
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"}
    }
}

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
        validate(data, SIGNUP_SCHEMA)

        for key in data.keys():
            if data[key].isspace():
                return {'error': 'values cannot be empty strings'}, 400

        new_user = Users(data['first_name'], data['last_name'],
                         data['email'], data['password'])

        response = new_user.signup()

        return response

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
        validate(data, LOGIN_SCHEMA)

        for key in data.keys():
            if data[key].isspace():
                return {'error': "values cannot be empty strings"}, 400

        email = data['email']
        password = data['password']

        response = Users.login(email, password)

        return response
      