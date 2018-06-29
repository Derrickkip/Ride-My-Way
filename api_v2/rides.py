"""
Implements the rides endpoints
"""
import urllib.parse
import psycopg2
from flask import request, abort
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()

RESULT = urllib.parse.urlparse("postgresql://testuser:testuser@localhost/testdb")
USERNAME = RESULT.username
DATABASE = RESULT.path[1:]
HOSTNAME = RESULT.hostname
PASSWORD = RESULT.password


class Rides(Resource):
    @jwt_required
    def get(self):
        """
        fetch all rides
        """        
        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                        password=PASSWORD, host=HOSTNAME)

        cur = conn.cursor()

        cur.execute('select * from rides')

        rows = cur.fetchall()

        rides = {}
        for row in rows:
            rides[1] = row

        return {'rides': rides }, 200


class Ride(Resource):
    @jwt_required
    def get(self, ride_id):
        """
        fetch single ride
        """
        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                        password=PASSWORD, host=HOSTNAME)

        cur = conn.cursor()

        cur.execute('select * from rides where ride_id=%(ride_id)s', {'ride_id':ride_id})

        rows = cur.fetchone()

        return {'ride': rows}

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


