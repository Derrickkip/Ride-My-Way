"""
Fixtures for tests
"""
import datetime
import time
import pytest

from app.models import Users, Rides

@pytest.fixture(scope='module')
def new_user():
    """
    Create Instance of User class to be used by the module
    """
    user = Users('Daudi', 'Jesee', 'dj@mail.com', 'password')
    return user

@pytest.fixture(scope='module')
def new_ride():
    """
    Create new ride instance
    """
    ride = Rides('Nairobi', 'Mombasa', datetime.date(2018, 8, 17), time.strftime("%H %M"),
                 '500 kshs')
    return ride
