"""
Fixtures for tests
"""
import datetime
import pytest

from app.models import Users, Rides

@pytest.fixture(scope='module')
def new_user():
    """
    Create Instance of User class to be used by the module
    """
    user_details = ['Daudi', 'Jesee', 'dj@mail.com', 'password']
    user = Users(user_details)
    return user

@pytest.fixture(scope='module')
def new_ride():
    """
    Create new ride instancec
    """
    date = datetime.date.today()
    travel_time = datetime.time(1, 2, 3)
    date_of_travel = datetime.datetime.combine(date, travel_time)
    ride = Rides('Nairobi', 'Mombasa', date_of_travel, '500 kshs')
    return ride
