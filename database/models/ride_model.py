"""
Ride model
Implements CRUD operations for rides
"""
from flask import abort
from flask_jwt_extended import get_jwt_identity
from ..dbconn import dbconn
from .helpers import (get_user_by_email, get_user_car, get_user_by_id, get_phone_number,
                      get_ride_owner, check_requestor, get_ride_details, check_ride_existence)

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
            abort(400, 'Update your car details to create ride')

        message, code = check_ride_existence(user[0], self.date_of_ride, self.time)

        if message:
            return message, code

        conn = dbconn()
        cur = conn.cursor()

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
        cur.execute('''select ride_id, origin, destination, date_of_ride,
                        time, price, user_id from rides''')

        rows = cur.fetchall()

        rides = []
        for row in rows:
            ride = {
                'id':row[0],
                'origin':row[1],
                'destination': row[2],
                'date_of_ride': row[3],
                'time': row[4],
                'price': row[5],
                'driver': get_user_by_id(row[6])
            }
            rides.append(ride)

        cur.close()
        conn.close()

        if rides == []:
            return {'message': 'No rides available'}

        return rides, 200

    @staticmethod
    def get_single_ride(ride_id):
        """
        get single ride method
        """
        conn = dbconn()
        cur = conn.cursor()
        cur.execute('''select ride_id, user_id, origin, destination,
                        date_of_ride, time, price, requests
                        from rides where ride_id=%(ride_id)s''', {'ride_id':ride_id})

        rows = cur.fetchone()
        if not rows:
            abort(404, 'ride not found')

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
            'seats': car[4], 'requests': rows[7]
        }

        cur.close()
        conn.close()

        return {'ride': ride}

    @staticmethod
    def update_ride(ride_id, data):
        """
        update ride method
        """
        email = get_jwt_identity()

        #Only the ride creater should be able to update ride
        message, code = check_requestor(email, ride_id)

        if message:
            return message, code

        row = get_ride_details(ride_id)

        origin = row[0]
        destination = row[1]
        date_of_ride = row[2]
        time = row[3]
        price = row[4]

        conn = dbconn()
        cur = conn.cursor()

        cur.execute('''update rides set origin=%(origin)s, destination=%(destination)s,
                        date_of_ride=%(date_of_ride)s, time=%(time)s,
                        price=%(price)s where ride_id=%(ride_id)s''',
                    {'origin': data.get('origin', origin),
                     'destination': data.get('destination', destination),
                     'date_of_ride': data.get('date_of_ride', date_of_ride),
                     'time': data.get('time', time),
                     'price': data.get('price', price), 'ride_id': ride_id})

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
            abort(404, 'Ride not found')
        if user != ride_owner[0]:
            abort(403, 'You dont have permission to perform this operation')

        conn = dbconn()
        cur = conn.cursor()
        cur.execute('''delete from rides where ride_id=%(ride_id)s''',
                    {'ride_id': ride_id})

        cur.close()
        conn.commit()
        conn.close()


        return {'success':'ride deleted'}, 200
