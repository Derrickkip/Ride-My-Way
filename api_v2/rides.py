"""
Implements the rides endpoints
"""
import urllib.parse
import psycopg2
from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()

RESULT = urllib.parse.urlparse("postgresql://testuser:testuser@localhost/testdb")
USERNAME = RESULT.username
DATABASE = RESULT.path[1:]
HOSTNAME = RESULT.hostname
PASSWORD = RESULT.password

def get_user_by_email(email):
    """
    returns user with given email
    """
    conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                            password=PASSWORD, host=HOSTNAME)

    cur = conn.cursor()

    cur.execute("select user_id, first_name from users where email=%(email)s", {'email':email})

    rows = cur.fetchone()

    cur.close()

    conn.commit()

    conn.close()


    return rows

def get_user_by_id(user_id):
    """
    return user name for user with given id
    """
    conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                            password=PASSWORD, host=HOSTNAME)

    cur = conn.cursor()

    cur.execute("select first_name, last_name from users where user_id=%(user_id)s",
                {'user_id':user_id})

    rows = cur.fetchone()
    full_name = rows[0] +' '+ rows[1]

    cur.close()

    conn.commit()

    conn.close()


    return full_name


class Rides(Resource):
    """
    returns list of rides
    """
    @jwt_required
    def get(self):
        """
        fetch all rides
        """
        self.conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                password=PASSWORD, host=HOSTNAME)

        self.cur = self.conn.cursor()

        self.cur.execute('select ride_id, origin, destination, date_of_ride, time, price, user_id from rides')

        self.rows = self.cur.fetchall()

        self.rides = {}
        num = 1
        for row in self.rows:
            self.rides[num] = {
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

        self.conn.commit()

        self.conn.close()

        return {'rides': self.rides}, 200


class Ride(Resource):
    """
    returns a single ride specified by id
    """
    @jwt_required
    def get(self, ride_id):
        """
        fetch single ride
        """
        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                password=PASSWORD, host=HOSTNAME)

        cur = conn.cursor()

        cur.execute('select ride_id, user_id, origin, destination, date_of_ride, time, price from rides where ride_id=%(ride_id)s', {'ride_id':ride_id})

        rows = cur.fetchone()

        ride = {
            'id': rows[0],
            'driver': get_user_by_id(rows[1]),
            'origin': rows[2],
            'destination': rows[3],
            'date_of_ride': rows[4],
            'time': rows[5],
            'price': rows[6]
        }

        cur.close()

        conn.commit()

        conn.close()

        return {'ride': ride}

class CreateRide(Resource):
    """
    Create new ride
    """
    @jwt_required
    def post(self):
        """
        create a new ride
        """
        parser.add_argument('origin', type=str, help='where ride is from')
        parser.add_argument('destination', type=str, help='where ride is headed')
        parser.add_argument('date_of_ride', type=str, help='day of ride')
        parser.add_argument('time', type=str, help='time of trave')
        parser.add_argument('price', type=int, help='how much one has to pay for ride')
        args = parser.parse_args()

        origin = args['origin']
        destination = args['destination']
        date_of_ride = args['date_of_ride']
        time = args['time']
        price = args['price']

        email = get_jwt_identity()
        user = get_user_by_email(email)

        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                password=PASSWORD, host=HOSTNAME)

        cur = conn.cursor()

        #check that user has not created the same ride twice

        cur.execute("select date_of_ride, time from rides where user_id=%(user_id)s",{'user_id':user[0]})
        
        row = cur.fetchone()
        if row:
            ride_date = row[0]
            ride_time = row[1]

            if (ride_date==date_of_ride) and (ride_time==time):
                abort(400)

        cur.execute("""INSERT INTO rides (origin, destination, date_of_ride, time, 
                    price, user_id) VALUES(%s, %s, %s, %s, %s, %s)""",
                    [origin, destination, date_of_ride, time, price, user[0]])
        
        cur.close()

        conn.commit()

        conn.close()

        return {'success': 'ride created'}, 201

class MakeRequest(Resource):
    """
    request for ride
    """
    @jwt_required
    def post(self, ride_id):
        """
        request a ride
        """
        email = get_jwt_identity()
        user = get_user_by_email(email)
        
        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                password=PASSWORD, host=HOSTNAME)

        cur = conn.cursor()

        cur.execute("select ride_id from requests where user_id=%(user_id)s", {'user_id': user[0]})

        row = cur.fetchone()

        if row:

            if row[0] == ride_id:
                abort(400)

        cur.execute("insert into requests (user_id, ride_id) values (%s, %s)", [user[0], ride_id])

        cur.close()

        conn.commit()

        conn.close()

        return {'success':'You have successfully requested for the ride'}, 200

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


