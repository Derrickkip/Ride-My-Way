"""
Car model
Implement CRUD functionality for Cars resource
"""
from flask import abort
from flask_jwt_extended import get_jwt_identity
from ..dbconn import dbconn
from .helpers import get_user_by_email, get_user_car, registration_exists

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
            abort(400, 'You can only use one car')

        if registration_exists(self.registration):
            abort(400, 'That registration already exists')

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
            abort(404, 'No car found')

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
            abort(404, 'Car not found')
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
            abort(404, 'Car not found')
        conn = dbconn()

        cur = conn.cursor()

        cur.execute('''delete from cars where user_id=%(user_id)s''',
                    {'user_id': user_id})

        cur.close()

        conn.commit()

        conn.close()

        return {'message': 'car details deleted'}
