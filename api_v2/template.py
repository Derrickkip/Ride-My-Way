'''
Swagger template
'''

TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Ride-My-Way",
        "description": 'Ride-My-Way is a carpooling app that allows drivers to \
                        create ride offers and passengers to join available ride offers',
    },
    "securityDefinitions":{
        "Bearer":{
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "definitions":{
        "UserSignup":{
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string"
                },
                "last_name": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            }
        },
        "UserLogin": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            }
        },
        "Rides": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string"
                },
                "destination": {
                    "type": "string"
                },
                "date_of_ride": {
                    "type": "string"
                },
                "time": {
                    "type": "string"
                },
                "price": {
                    "type": "number"
                }
            }
        },
        "Requests": {
            "type": "object",
            "properties": {
                "request_id": {
                    "type": "number"
                },
                "username": {
                    "type": "string"
                },
                "status": {
                    "type": "string"
                }
            }
        },
        "Response": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["rejected", "accepted"]
                }
            }
        }
    }
}
    