"""
Tests for app models
"""
import datetime

def test_user_model(new_user):
    """
    test that user can create account
    """
    assert new_user.is_driver is False
    assert new_user.first_name == 'Daudi'
    assert new_user.last_name == 'Jesee'
    assert new_user.email == 'dj@mail.com'
    assert new_user.hashed_password != 'password'
    assert new_user.car_details is None
    assert str(new_user) == 'Daudi Jesee'

def test_driver_model(new_driver):
    """
    test that driver instance is created correctly
    """
    assert new_driver.is_driver is True
    assert new_driver.first_name == 'Daudi'
    assert new_driver.last_name == 'Jesee'
    assert new_driver.email == 'dj@mail.com'
    assert new_driver.hashed_password != 'password'
    assert new_driver.driving_licence == 2413e443541
    assert new_driver.car_model == 'Mitsubishi Lancer'
    assert new_driver.car_registration_number == 'KBX 001'
    assert new_driver.seats_available == 4

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

def test_request_class(new_request):
    """
    test request instance
    """
    assert str(new_request.user) == 'Daudi Jesee'
    accept = new_request.accept()
    assert "Request from Daudi Jesee Accepted" in accept
    reject = new_request.reject()
    assert "Request from Daudi Jesee Rejected" in reject
