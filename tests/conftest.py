"""
Fixtures for tests
"""
import pytest

from app.models import User

@pytest.fixture(scope='module')
def new_user():
    """
    Create Instance of User class to be used by the module
    """
    user = User('Daudi', 'Jesee', 'dj@mail.com', 'password')
    return user
