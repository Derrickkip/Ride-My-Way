"""
Fixtures for tests
"""
import pytest

from app import create_app

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
