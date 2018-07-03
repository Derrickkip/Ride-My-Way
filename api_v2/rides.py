"""
Implements the rides endpoints
"""
import urllib.parse
import psycopg2
from flask import request
from flask_restful import Resource
from jsonschema import validate
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.dbsetup import dbconn

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

def get_user_by_email(email):
    """
    returns user with given email
    """
    try:
        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''select
                    user_id,
                    first_name from users where email=%(email)s''', {'email':email})

        rows = cur.fetchone()

        cur.close()
        conn.close()

        return rows

    except psycopg2.DatabaseError as error:
        return {'error': str(error)}

def get_user_by_id(user_id):
    """
    return user name for user with given id
    """
    try:
        conn = dbconn()
        cur = conn.cursor()

        cur.execute("select first_name, last_name from users where user_id=%(user_id)s",
                    {'user_id':user_id})

        rows = cur.fetchone()
        full_name = rows[0] +' '+ rows[1]

        cur.close()
        conn.close()

        return full_name

    except psycopg2.DatabaseError as error:
        return {'error': str(error)}

def get_ride_owner_by_ride_id(ride_id):
    """
    returns ride with specified id
    """
    try:
        conn = dbconn()
        cur = conn.cursor()

        cur.execute('''select
                    user_id from rides where ride_id=%(ride_id)s''',
                    {'ride_id': ride_id})

        rows = cur.fetchone()

        cur.close()
        conn.close()

        return rows[0]

    except psycopg2.DatabaseError as error:
        return {'error': str(error)}

class Rides(Resource):
    """
    handler for /rides endpoint
    """
    def __init__(self):
        self.conn = dbconn()
        self.cur = self.conn.cursor()

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

        try:
            self.cur.execute('''select
                            ride_id,
                            origin,
                            destination,
                            date_of_ride,
                            time,
                            price,
                            user_id from rides''')

            rows = self.cur.fetchall()

            rides = {}
            num = 1
            for row in rows:
                rides[num] = {
                    'id':row[0],
                    'origin':row[1],
                    'destinaton': row[2],
                    'date_of_ride': row[3],
                    'time': row[4],
                    'price': row[5],
                    'driver': get_user_by_id(row[6])
                }
                num += 1

            self.cur.close()
            self.conn.close()

            return {'rides': rides}, 200

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

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

        origin = data['origin']
        destination = data['destination']
        date_of_ride = data['date_of_ride']
        time = data['time']
        price = data['price']

        email = get_jwt_identity()
        user = get_user_by_email(email)

        try:
            #check that user has not created the same ride twice
            self.cur.execute('''select
                            date_of_ride,
                            time
                            from rides where user_id=%(user_id)s''',
                             {'user_id':user[0]})

            row = self.cur.fetchone()
            if row:
                ride_date = row[0]
                ride_time = row[1]

                if (ride_date == date_of_ride) and (ride_time == time):
                    return {'bad request': 'You have already created a ride at that time'}, 400
            #insert ride to database

            self.cur.execute('''insert into rides
                            (origin,
                            destination,
                            date_of_ride,
                            time, 
                            price, user_id) VALUES(%s, %s, %s, %s, %s, %s)''',
                             [origin, destination, date_of_ride, time, price, user[0]])

            self.cur.close()
            self.conn.commit()
            self.conn.close()

            return {'success': 'ride created'}, 201

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}


class Ride(Resource):
    """
    Single ride operations
    """
    def __init__(self):
        self.conn = dbconn()
        self.cur = self.conn.cursor()

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
        try:
            self.cur.execute('''select ride_id,
                            user_id,
                            origin,
                            destination,
                            date_of_ride,
                            time,
                            price
                            from rides where ride_id=%(ride_id)s''', {'ride_id':ride_id})

            rows = self.cur.fetchone()
            if not rows:
                return {'error': 'ride not found'}, 404

            ride = {
                'id': rows[0],
                'driver': get_user_by_id(rows[1]),
                'origin': rows[2],
                'destination': rows[3],
                'date_of_ride': rows[4],
                'time': rows[5],
                'price': rows[6]
            }

            self.cur.close()
            self.conn.close()

            return {'ride': ride}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

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
        #Only the ride creater should be able to update ride
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner_by_ride_id(ride_id)

        if ride_owner is None:
            return {'error': 'ride not found'}, 404

        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403
        try:
            self.cur.execute('''select
                            origin,
                            destination,
                            date_of_ride,
                            time,
                            price from rides where ride_id=%(ride_id)s''',
                             {'ride_id':ride_id})

            row = self.cur.fetchone()
            if not row:
                return {'request error': 'ride not found'}, 404

            origin = row[0]
            destination = row[1]
            date_of_ride = row[2]
            time = row[3]
            price = row[4]

            self.cur.execute('''update rides set
                            origin=%(origin)s, 
                            destination=%(destination)s,
                            date_of_ride=%(date_of_ride)s,
                            time=%(time)s,
                            price=%(price)s where ride_id=%(ride_id)s''',
                             {'origin': request.json.get('origin', origin),
                              'destination': request.json.get('destination', destination),
                              'date_of_ride': request.json.get('date_of_ride', date_of_ride),
                              'time': request.json.get('time', time),
                              'price': request.json.get('price', price),
                              'ride_id': ride_id})

            self.cur.close()
            self.conn.commit()
            self.conn.close()

            return {'success': 'ride details updated'}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

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
              description: Id of ride to update
        responses:
            200:
                description: ride deleted
            404:
                description: ride not found

        """
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner_by_ride_id(ride_id)
        if ride_owner is None:
            return {'error':'Ride not found'}, 404
        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        try:
            self.cur.execute('''delete from rides where ride_id=%(ride_id)s''',
                             {'ride_id': ride_id})

            self.cur.close()
            self.conn.commit()
            self.conn.close()

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

        return {'success':'ride deleted'}, 200

class Requests(Resource):
    """
    Requests operations
    """
    def __init__(self):
        self.conn = dbconn()
        self.cur = self.conn.cursor()

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
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner_by_ride_id(ride_id)

        if ride_owner is None:
            return {'error': 'ride not found'}, 404

        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        try:
            self.cur.execute('''select
                            request_id,
                            user_id,
                            accept_status
                            from requests where ride_id=%(ride_id)s''',
                             {'ride_id': ride_id})

            rows = self.cur.fetchall()
            requests = {}
            num = 1
            for row in rows:
                requests[num] = {
                    'id':row[0],
                    'user_name': get_user_by_id(row[1]),
                    'accept_status': row[2]
                }
                num += 1
            self.cur.close()
            self.conn.close()

            return requests

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

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
        email = get_jwt_identity()
        user = get_user_by_email(email)
        ride = get_ride_owner_by_ride_id(ride_id)

        if ride is None:
            return {"error": "ride not found"}, 404

        try:
            #check that user has not requested for the ride
            self.cur.execute('''select
                            ride_id
                            from requests where user_id=%(user_id)s''',
                             {'user_id': user[0]})

            row = self.cur.fetchone()

            if row:
                if row[0] == ride_id:
                    return {'bad request': 'you have already requested for this ride'}, 400
            self.cur.execute('''insert into requests (user_id, ride_id) values (%s, %s)''',
                             [user[0], ride_id])

            self.cur.close()
            self.conn.commit()
            self.conn.close()

            return {'success':'You have successfully requested for the ride'}, 200

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

class Respond(Resource):
    '''
    User should be able to accept or reject a request for ride
    '''
    def __init__(self):
        self.conn = dbconn()
        self.cur = self.conn.cursor()

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

        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner_by_ride_id(ride_id)
        if not ride_owner:
            return {'error': 'ride not found'}, 404
        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        try:
            self.cur.execute('''update requests
                            set accept_status =%(accept_status)s 
                            where request_id =%(request_id)s''',
                             {'accept_status':data['status'], 'request_id': request_id})

            self.cur.close()
            self.conn.commit()
            self.conn.close()

            return {'success': 'request has been updated'}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}
