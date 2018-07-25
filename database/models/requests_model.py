"""
Request model
Implements Get requests, Make requests and Respond to requests
"""
from flask import abort
from flask_jwt_extended import get_jwt_identity
from ..dbconn import dbconn
from .helpers import (get_user_by_email, get_ride_owner, get_user_by_id,
                      get_user_car, check_requestor)

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
        message, code = check_requestor(email, ride_id)

        if message:
            return message, code

        conn = dbconn()
        cur = conn.cursor()
        cur.execute('''select
                        request_id, user_id, accept_status
                        from requests where ride_id=%(ride_id)s''',
                    {'ride_id': ride_id})

        rows = cur.fetchall()
        requests = {}
        num = 1
        for row in rows:
            requests[num] = {
                'id':row[0], 'user_name': get_user_by_id(row[1]),
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
            abort(404, "ride not found")

        conn = dbconn()
        cur = conn.cursor()

        #check that the requestor is not the owner of the ride
        cur.execute('''select user_id, requests
                        from rides where ride_id=%(ride_id)s''', {'ride_id': ride_id})
        row = cur.fetchone()
        if row[0] == user[0]:
            abort(400, "You cannot request your own ride")

        #check that the requests are not more than the seats
        requests = row[1]
        seats = get_user_car(row[0])[4]

        if requests >= seats:
            abort(400, "The ride is fully booked")

        #check that user has not requested for the ride
        cur.execute('''select ride_id, user_id
                        from requests where user_id=%(user_id)s''', {'user_id': user[0]})

        rows = cur.fetchall()
        if rows:
            for row in rows:
                if row[0] == ride_id:
                    abort(400, 'you have already requested for this ride')



        cur.execute('''insert into requests (user_id, ride_id) values (%s, %s)''',
                    [user[0], ride_id])

        cur.execute('''update rides set requests=%(requests)s where ride_id=%(ride_id)s''',
                    {'requests': requests+1, 'ride_id': ride_id})

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
            abort(404, 'ride not found')
        if user != ride_owner[0]:
            abort(403, 'You dont have permission to perform this operation')

        conn = dbconn()
        cur = conn.cursor()
        cur.execute('''select * from requests where request_id=%(request_id)s''',
                    {'request_id': request_id})

        row = cur.fetchone()

        if not row:
            abort(404, 'That request does not exist')

        cur.execute('''update requests
                        set accept_status =%(accept_status)s 
                        where request_id =%(request_id)s''',
                    {'accept_status':data['status'], 'request_id': request_id})

        cur.close()
        conn.commit()
        conn.close()

        return {'success': 'request has been updated'}
