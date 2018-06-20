"""
Tests for app models
"""
import datetime
import time

def test_user_model(new_user):
    """
    test that user can create account
    """
    assert new_user.first_name == 'Daudi'
    assert new_user.last_name == 'Jesee'
    assert new_user.email == 'dj@mail.com'
    assert new_user.hashed_password != 'password'
    assert new_user.car_details is None

def test_ride_model(new_ride):
    """
    test instance of ride class created correctly
    """
    assert new_ride.origin == "Nairobi"
    assert new_ride.destination == "Mombasa"
    assert new_ride.date == datetime.date(2018, 8, 17)
    assert new_ride.time == time.strftime("%H %M")
    assert new_ride.price == "500 kshs"
    