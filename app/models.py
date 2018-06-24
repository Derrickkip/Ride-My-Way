"""
Defines mock data to be used by api
"""

RIDES = [
    {
        'id': 1,
        'driver': 'Michael Owen',
        'origin': 'Mombasa',
        'destination': 'Nairobi',
        'travel_date': '23th June 2018',
        'time': '10:00 am',
        'car_model': 'Mitsubishi Evo 8',
        'seats': 4,
        'price': 500,
        'requests': []
    },
    {
        'id': 2,
        'driver': 'Sam West',
        'origin': 'Kisumu',
        'destination': 'Lodwar',
        'travel_date': '25th June 2018',
        'time': '12:00 am',
        'car_model':'Subaru Imprezza',
        'seats':3,
        'price': 400,
        'requests': []
    }
]

USERS = [
    {
        "id" : 1,
        'first_name': 'Michael',
        'last_name': 'Owen',
        'user_name': 'Mike',
        'email': 'micowen@mail.com',
        'driver_details' : {
            'driving_license': 'fdwer2ffew3',
            'car_model' : 'Mitsubishi Evo 8',
            'plate_number': 'KYT 312X',
            'seats': 4,
        },
        'rides_offered' : 1,
        'rides_requested' : 0
    },
    {
        'id': 2,
        'first_name': 'Wendy',
        'last_name': 'Kim',
        'user_name': 'wendesky',
        'email': 'wendesky@mail.com',
        'driver_details' : {},
        'rides_offered' : 0,
        'rides_requested' : 1
    }
]
