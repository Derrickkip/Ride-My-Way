"""
Fixture for api v2 tests
"""
import pytest

from apiV2 import app

@pytest.fixture(scope='module')
def test_client():
    """
    setup test client for module
    """
    app_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield app_client

    ctx.push

