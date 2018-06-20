"""
Tests for app models
"""

def test_user_model(new_user):
    """
    test that user can create account
    """
    assert new_user.first_name == 'Daudi'
    assert new_user.last_name == 'Jesee'
    assert new_user.email == 'dj@mail.com'
    assert new_user.hashed_password != 'password'
    assert new_user.car_details is None
