'''
API Schema defitions
'''

SIGNUP_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "password": {"type": "string"},
        "confirm_password": {"type": "string"}
    },
    "required": ["first_name", "last_name", "email", "phone_number", "password", "confirm_password"]
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required":['email', 'password']
}

RIDE_SCHEMA = {
    "type": "object",
    "properties": {
        "origin": {"type": "string"},
        "destination": {"type": "string"},
        "date_of_ride": {"type": "string"},
        "time": {"type": "string"},
        "price": {"type": "number"}
    },
    "required": [
        "origin",
        "destination",
        "date_of_ride",
        "time",
        "price"
    ]
}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"enum": ["accepted", "rejected"]}
    },
    "required": ["status"]
}

CAR_SCHEMA = {
    "type": "object",
    "properties": {
        "car_model": {"type": "string"},
        "registration": {"type": "string"},
        "seats": {"type": "number"}
    },
    "required": [
        "car_model",
        "registration",
        "seats"
    ]
}
