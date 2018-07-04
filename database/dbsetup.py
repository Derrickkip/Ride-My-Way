"""
Database config
"""

import psycopg2
from flask import current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity

def dbconn():
    """
    return db connector
    """
    conn = psycopg2.connect(current_app.config['DATABASE'])

    return conn

########################################
# HELPER METHODS
########################################

def get_user_by_email(email):
    """
    returns user with given email
    """
    try:
        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''select * from users where email=%(email)s''', {'email':email})

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

def get_ride_owner(ride_id):
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

def get_user(email):
    """
    Method to check if user exists in db
    """
    conn = dbconn()

    cur = conn.cursor()

    cur.execute("select * from users where email=%(email)s", {'email':email})

    rows = cur.fetchone()

    cur.close()

    conn.close()

    return rows is not None

def get_password(email):
    """
    get users password
    """
    conn = dbconn()
    cur = conn.cursor()

    cur.execute('''SELECT password FROM users WHERE email=%(email)s''',
                {'email':email})

    rows = cur.fetchone()

    return rows

########################################

class Users(object):
    """
    user class definition
    """
    def __init__(self, first_name, last_name, email, password, carmodel=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.carmodel = carmodel

    def signup(self):
        """
        user signup method
        """

        data = [self.first_name, self.last_name, self.email, self.password_hash, self.carmodel]

        if get_user(self.email):
            return {'error': 'user already exists'}, 400

        try:

            conn = dbconn()
            cur = conn.cursor()

            sql = """INSERT INTO users (first_name, last_name, email, password, carmodel)
                        VALUES(%s, %s, %s, %s, %s)"""

            cur.execute(sql, data)

            cur.close()

            conn.commit()

            conn.close()

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

        return {'success': 'user account created'}, 201

    @staticmethod
    def login(email, password):
        """
        login method
        """
        if get_user(email):
            try:

                stored_password = get_password(email)[0]

                if check_password_hash(stored_password, password):
                    access_token = create_access_token(email)

                    return {"success":"login successful",
                            "access_token": access_token}

            except psycopg2.DatabaseError as error:
                return jsonify({'error': str(error)})


        return {'error':'The email is not recognised'}, 404

class Rides(object):
    """
    Rides object implementation
    """
    def __init__(self, origin, destination, date_of_ride, time, price):
        self.origin = origin
        self.destination = destination
        self.date_of_ride = date_of_ride
        self.time = time
        self.price = price

    def create_ride(self):
        """
        create new ride method
        """
        email = get_jwt_identity()
        user = get_user_by_email(email)

        try:
            conn = dbconn()
            cur = conn.cursor()
            #check that user has not created the same ride twice
            cur.execute('''select
                            date_of_ride,
                            time
                            from rides where user_id=%(user_id)s''',
                        {'user_id':user[0]})

            row = cur.fetchone()
            if row:
                ride_date = row[0]
                ride_time = row[1]

                if (ride_date == self.date_of_ride) and (ride_time == self.time):
                    return {'bad request': 'You have already created a ride at that time'}, 400
            #insert ride to database

            cur.execute('''insert into rides
                            (origin,
                            destination,
                            date_of_ride,
                            time, 
                            price, user_id) VALUES(%s, %s, %s, %s, %s, %s)''',
                        [self.origin, self.destination, self.date_of_ride, self.time,
                         self.price, user[0]])

            cur.close()
            conn.commit()
            conn.close()

            return {'success': 'ride created'}, 201

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def get_all_rides():
        """
        get al rides methods
        """
        try:
            conn = dbconn()
            cur = conn.cursor()
            cur.execute('''select
                            ride_id,
                            origin,
                            destination,
                            date_of_ride,
                            time,
                            price,
                            user_id from rides''')

            rows = cur.fetchall()

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

            cur.close()
            conn.close()

            return {'rides': rides}, 200

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def get_single_ride(ride_id):
        """
        get single ride method
        """
        try:
            conn = dbconn()
            cur = conn.cursor()
            cur.execute('''select ride_id,
                            user_id,
                            origin,
                            destination,
                            date_of_ride,
                            time,
                            price
                            from rides where ride_id=%(ride_id)s''', {'ride_id':ride_id})

            rows = cur.fetchone()
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

            cur.close()
            conn.close()

            return {'message':'success', 'ride': ride}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def update_ride(ride_id, data):
        """
        update ride method
        """
        #Only the ride creater should be able to update ride
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner(ride_id)

        if ride_owner is None:
            return {'error': 'ride not found'}, 404

        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403
        try:
            conn = dbconn()
            cur = conn.cursor()
            cur.execute('''select
                            origin,
                            destination,
                            date_of_ride,
                            time,
                            price from rides where ride_id=%(ride_id)s''',
                        {'ride_id':ride_id})

            row = cur.fetchone()
            if not row:
                return {'request error': 'ride not found'}, 404

            origin = row[0]
            destination = row[1]
            date_of_ride = row[2]
            time = row[3]
            price = row[4]

            cur.execute('''update rides set
                            origin=%(origin)s, 
                            destination=%(destination)s,
                            date_of_ride=%(date_of_ride)s,
                            time=%(time)s,
                            price=%(price)s where ride_id=%(ride_id)s''',
                        {'origin': data.get('origin', origin),
                         'destination': data.get('destination', destination),
                         'date_of_ride': data.get('date_of_ride', date_of_ride),
                         'time': data.get('time', time),
                         'price': data.get('price', price),
                         'ride_id': ride_id})

            cur.close()
            conn.commit()
            conn.close()

            return {'success': 'ride details updated'}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def delete_ride(ride_id):
        """
        delete ride method
        """
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner(ride_id)
        if ride_owner is None:
            return {'error':'Ride not found'}, 404
        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        try:
            conn = dbconn()
            cur = conn.cursor()
            cur.execute('''delete from rides where ride_id=%(ride_id)s''',
                        {'ride_id': ride_id})

            cur.close()
            conn.commit()
            conn.close()

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

        return {'success':'ride deleted'}, 200

class Requests(object):
    """
    Request object implementation
    """
    def __init__(self, request_id, user_id, accept_status='pending'):
        self.request_id = request_id
        self.user_id = user_id
        self.accept_status = accept_status

    @staticmethod
    def get_all_requests(ride_id):
        """
        get all requests method
        """
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner(ride_id)

        if ride_owner is None:
            return {'error': 'ride not found'}, 404

        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        try:
            conn = dbconn()
            cur = conn.cursor()
            cur.execute('''select
                            request_id,
                            user_id,
                            accept_status
                            from requests where ride_id=%(ride_id)s''',
                        {'ride_id': ride_id})

            rows = cur.fetchall()
            requests = {}
            num = 1
            for row in rows:
                requests[num] = {
                    'id':row[0],
                    'user_name': get_user_by_id(row[1]),
                    'accept_status': row[2]
                }
                num += 1
            cur.close()
            conn.close()

            return requests

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def make_request(ride_id):
        """
        make request method
        """
        email = get_jwt_identity()
        user = get_user_by_email(email)
        ride = get_ride_owner(ride_id)

        if ride is None:
            return {"error": "ride not found"}, 404

        try:
            conn = dbconn()
            cur = conn.cursor()
            #check that user has not requested for the ride
            cur.execute('''select
                            ride_id
                            from requests where user_id=%(user_id)s''',
                        {'user_id': user[0]})

            row = cur.fetchone()

            if row:
                if row[0] == ride_id:
                    return {'bad request': 'you have already requested for this ride'}, 400
            cur.execute('''insert into requests (user_id, ride_id) values (%s, %s)''',
                        [user[0], ride_id])

            cur.close()
            conn.commit()
            conn.close()

            return {'success':'You have successfully requested for the ride'}, 200

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}

    @staticmethod
    def respond_to_request(ride_id, request_id, data):
        """
        reject or accept request method
        """
        email = get_jwt_identity()
        user = get_user_by_email(email)[0]
        ride_owner = get_ride_owner(ride_id)
        if not ride_owner:
            return {'error': 'ride not found'}, 404
        if user != ride_owner:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        try:
            conn = dbconn()
            cur = conn.cursor()
            cur.execute('''update requests
                            set accept_status =%(accept_status)s 
                            where request_id =%(request_id)s''',
                        {'accept_status':data['status'], 'request_id': request_id})

            cur.close()
            conn.commit()
            conn.close()

            return {'success': 'request has been updated'}

        except psycopg2.DatabaseError as error:
            return {'error': str(error)}
