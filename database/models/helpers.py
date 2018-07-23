'''
Helper methods for models
'''
from ..dbconn import dbconn

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

def check_requestor(email, ride_id):
    """
    Check requester against ride_owner
    """
    user = get_user_by_email(email)[0]
    ride_owner = get_ride_owner(ride_id)
    message = None
    code = None

    if ride_owner is None:
        message = {'error': 'ride not found'}
        code = 404

    elif user != ride_owner[0]:
        message = {'forbidden': 'You dont have permission to perform this operation'}
        code = 403

    return message, code

def get_ride_details(ride_id):
    """
    Get details of ride with id
    """
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

    return row

def check_ride_existence(user_id, date_of_ride, time):
    """
    Check user has not created ride at same time
    """

    message = None
    code = None
    conn = dbconn()
    cur = conn.cursor()
    #check that user has not created the same ride twice
    cur.execute('''select
                    date_of_ride,
                    time
                    from rides where user_id=%(user_id)s''',
                {'user_id':user_id})

    rows = cur.fetchall()
    if rows:
        for row in rows:
            ride_date = row[0]
            ride_time = row[1]

            if (ride_date == date_of_ride) and (ride_time == time):
                message = {'bad request': 'You have already created a ride at that time'}
                code = 400

    return message, code

def update_ride_requests(requests, ride_id):
    """
    Updates number of requests after each request
    """
    conn = dbconn()
    cur = conn.cursor()
    cur.execute('''update rides set requests=%(requests)s where ride_id=%(ride_id)s''',
                {'requests': requests+1, 'ride_id': ride_id})

    cur.close()
    conn.commit()
    conn.close()
