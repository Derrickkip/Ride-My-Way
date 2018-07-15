"""
Database config
"""
import psycopg2
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity

def dbconn():
    """
    return db connector
    """
    try:
        conn = psycopg2.connect(current_app.config['DATABASE'])

        return conn
    except psycopg2.DatabaseError as error:
        return {'error': str(error)}

########################################
# HELPER METHODS
########################################

def get_user_by_email(email):
    """
    returns user with given email
    """

    conn = dbconn()

    cur = conn.cursor()

    cur.execute('''select * from users where email=%(email)s''', {'email':email})

    rows = cur.fetchone()

    cur.close()
    conn.close()

    return rows

def get_user_by_id(user_id):
    """
    return user name for user with given id
    """
    conn = dbconn()
    cur = conn.cursor()

    cur.execute("select first_name, last_name from users where user_id=%(user_id)s",
                {'user_id':user_id})

    rows = cur.fetchone()
    full_name = rows[0] +' '+ rows[1]

    cur.close()
    conn.close()

    return full_name

def get_ride_owner(ride_id):
    """
    returns ride with specified id
    """
    conn = dbconn()
    cur = conn.cursor()

    cur.execute('''select
                user_id from rides where ride_id=%(ride_id)s''',
                {'ride_id': ride_id})

    rows = cur.fetchone()

    cur.close()
    conn.close()

    return rows

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

def get_phone_number(user_id):
    """
    returns users phone number
    """
    conn = dbconn()

    cur = conn.cursor()

    cur.execute("select phone_number from users where user_id=%(user_id)s", {'user_id':user_id})

    rows = cur.fetchone()

    cur.close()

    conn.close()

    return rows[0]

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

def get_user_car(user_id):
    """
    returns users  car
    """
    conn = dbconn()
    cur = conn.cursor()

    cur.execute('''SELECT * from cars where user_id=%(user_id)s''',
                {'user_id': user_id})

    row = cur.fetchone()

    return row

def registration_exists(registration):
    """
    Check that the car registration is unique
    """
    conn = dbconn()
    cur = conn.cursor()

    cur.execute('''SELECT * from cars where registration=%(registration)s''',
                {'registration': registration})

    row = cur.fetchone()

    return row is not None

########################################

class Users:
    """
    user class definition
    """
    def __init__(self, first_name, last_name, email, phone_number, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password_hash = generate_password_hash(password)

    def signup(self):
        """
        user signup method
        """

        data = [self.first_name, self.last_name, self.email, self.phone_number, self.password_hash]

        if get_user(self.email):
            return {'error': 'user already exists'}, 400

        conn = dbconn()
        cur = conn.cursor()

        sql = """INSERT INTO users (first_name, last_name, email, phone_number, password)
                    VALUES(%s, %s, %s, %s, %s)"""

        cur.execute(sql, data)

        cur.close()

        conn.commit()

        conn.close()

        return {'success': 'user account created'}, 201

    @staticmethod
    def login(email, password):
        """
        login method
        """
        if get_user(email):

            stored_password = get_password(email)[0]

            if not check_password_hash(stored_password, password):
                return {'error': 'Incorrect password, try again !'}, 400

            access_token = create_access_token(email)

            return {"success":"login successful",
                    "access_token": access_token}


        return {'error':'The email is not recognised'}, 404

class Rides:
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

        #check that user has car
        car = get_user_car(user[0])
        if car is None:
            return {'message': 'Update your car details to create ride'}, 400

        conn = dbconn()
        cur = conn.cursor()
        #check that user has not created the same ride twice
        cur.execute('''select
                        date_of_ride,
                        time
                        from rides where user_id=%(user_id)s''',
                    {'user_id':user[0]})

        rows = cur.fetchall()
        if rows:
            for row in rows:
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


    @staticmethod
    def get_all_rides():
        """
        get al rides methods
        """
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

        if rides == {}:
            return {'message': 'No rides available'}

        return {'rides': rides}, 200

    @staticmethod
    def get_single_ride(ride_id):
        """
        get single ride method
        """
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

        car = get_user_car(rows[1])

        ride = {
            'id': rows[0],
            'driver': get_user_by_id(rows[1]),
            'phone_number': get_phone_number(rows[1]),
            'origin': rows[2],
            'destination': rows[3],
            'date_of_ride': rows[4],
            'time': rows[5],
            'price': rows[6],
            'car_model': car[1],
            'registration': car[2],
            'seats': car[4]
        }

        cur.close()
        conn.close()

        return {'message':'success', 'ride': ride}

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

        if user != ride_owner[0]:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

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
        if user != ride_owner[0]:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        conn = dbconn()
        cur = conn.cursor()
        cur.execute('''delete from rides where ride_id=%(ride_id)s''',
                    {'ride_id': ride_id})

        cur.close()
        conn.commit()
        conn.close()


        return {'success':'ride deleted'}, 200

class Requests:
    """
    Request object implementation
    """
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

        if user != ride_owner[0]:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

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

        if requests == {}:
            return {'message': 'no requests yet'}

        return requests

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

        conn = dbconn()
        cur = conn.cursor()

        #check that the requestor is not the owner of the ride
        cur.execute('''select
                        user_id
                        from rides where ride_id=%(ride_id)s''',
                    {'ride_id': ride_id})
        row = cur.fetchone()
        if row[0] == user[0]:
            return {'error': 'You cannot request your own ride'}, 400

        #check that user has not requested for the ride
        cur.execute('''select
                        ride_id, user_id
                        from requests where user_id=%(user_id)s''',
                    {'user_id': user[0]})

        rows = cur.fetchall()
        if rows:
            for row in rows:
                if row[0] == ride_id:
                    return {'bad request': 'you have already requested for this ride'}, 400



        cur.execute('''insert into requests (user_id, ride_id) values (%s, %s)''',
                    [user[0], ride_id])

        cur.close()
        conn.commit()
        conn.close()

        return {'success':'You have successfully requested for the ride'}, 200

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
        if user != ride_owner[0]:
            return {'forbidden': 'You dont have permission to perform this operation'}, 403

        conn = dbconn()
        cur = conn.cursor()
        cur.execute('''select * from requests where request_id=%(request_id)s''',
                    {'request_id': request_id})

        row = cur.fetchone()

        if not row:
            return {'error': 'That request does not exist'}, 404

        cur.execute('''update requests
                        set accept_status =%(accept_status)s 
                        where request_id =%(request_id)s''',
                    {'accept_status':data['status'], 'request_id': request_id})

        cur.close()
        conn.commit()
        conn.close()

        return {'success': 'request has been updated'}

class Cars:
    """
    Car object implementation
    """
    def __init__(self, car_model, registration, seats):
        self.car_model = car_model
        self.registration = registration
        self.seats = seats

    def create_car(self):
        """
        create ride for user
        """
        email = get_jwt_identity()
        user_id = get_user_by_email(email)[0]

        #check user has no car
        car = get_user_car(user_id)
        if car:
            return {'message':'You can only use one car'}, 400

        if registration_exists(self.registration):
            return {'error': 'That registration already exists'}, 400

        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''insert into cars
                    (car_model, registration, user_id, seats)
                    values (%s,%s,%s, %s)''',
                    [self.car_model, self.registration, user_id, self.seats])

        cur.close()

        conn.commit()

        conn.close()

        return {'success': 'Car successfully added'}, 201

    @staticmethod
    def get_car():
        """
        fetch users car
        """
        email = get_jwt_identity()
        user_id = get_user_by_email(email)[0]
        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''select * from cars where user_id=%(user_id)s''', {'user_id': user_id})

        row = cur.fetchone()

        if row is None:
            return {'message': 'No car found'}, 404

        car = {}
        car['car_model'] = row[1]
        car['registration'] = row[2]
        car['seats'] = row[4]

        return {'car': car}

    @staticmethod
    def update_details(data):
        """
        Update user car details
        """
        email = get_jwt_identity()
        user_id = get_user_by_email(email)[0]

        car = get_user_car(user_id)
        if car is None:
            return {'error': 'Car not found'}, 404
        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''update cars set
                    car_model=%(car_model)s,
                    registration=%(registration)s,
                    seats=%(seats)s
                    where user_id=%(user_id)s''',
                    {'car_model': data['car_model'],
                     'registration': data['registration'],
                     'seats': data['seats'], 'user_id': user_id})

        cur.close()

        conn.commit()

        conn.close()

        return {'success': 'car details updated'}

    @staticmethod
    def delete():
        """
        delete car details
        """
        email = get_jwt_identity()
        user_id = get_user_by_email(email)[0]

        car = get_user_car(user_id)
        if car is None:
            return {'error': 'Car not found'}, 404
        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''delete from cars where user_id=%(user_id)s''',
                    {'user_id': user_id})

        cur.close()

        conn.commit()

        conn.close()

        return {'message': 'car details deleted'}
