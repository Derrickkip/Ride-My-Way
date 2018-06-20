"""
Tests for app models
"""
import datetime

def test_user_model(new_user):
    """
    test that user can create account
    """
    assert new_user.first_name == 'Daudi'
    assert new_user.last_name == 'Jesee'
    assert new_user.email == 'dj@mail.com'
    assert new_user.hashed_password != 'password'
    assert new_user.car_details is None
    assert str(new_user) == 'Daudi Jesee'

def test_ride_model(new_ride):
    """
    test instance of ride class created correctly
    """
    date = datetime.date.today()
    travel_time = datetime.time(1, 2, 3)
    date_of_travel = datetime.datetime.combine(date, travel_time)
    assert new_ride.origin == "Nairobi"
    assert new_ride.destination == "Mombasa"
    assert new_ride.travel_date == date_of_travel
    assert new_ride.price == "500 kshs"
    assert str(new_ride) == "Nairobi to Mombasa"
