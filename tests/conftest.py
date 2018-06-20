"""
Fixtures for tests
"""
import datetime
import pytest

from app import create_app

from app.models import Users, Drivers, Rides, Requests

@pytest.fixture(scope='module')
def test_client():
    """
    Flask test_client setup
    """
    app = create_app('testing')
    app_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield app_client

    ctx.pop()


@pytest.fixture(scope='module')
def new_user():
    """
    Create Instance of User class to be used by the module
    """
    user_details = ['Daudi', 'Jesee', 'dj@mail.com', 'password']
    user = Users(user_details)
    return user

@pytest.fixture(scope='module')
def new_driver():
    """
    Create Instance of Driver class
    """
    user_details = ['Daudi', 'Jesee', 'dj@mail.com', 'password']
    car_details = [2413e443541, 'Mitsubishi Lancer', 'KBX 001', 4]
    driver = Drivers(user_details, car_details)
    return driver

@pytest.fixture(scope='module')
def new_ride():
    """
    Create new ride instance
    """
    date = datetime.date.today()
    travel_time = datetime.time(1, 2, 3)
    date_of_travel = datetime.datetime.combine(date, travel_time)
    ride = Rides('Nairobi', 'Mombasa', date_of_travel, '500 kshs')
    return ride

@pytest.fixture(scope='module')
def new_request():
    """
    Create request instance
    """
    request = Requests(new_user())
    return request
