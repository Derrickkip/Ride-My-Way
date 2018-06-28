"""
Fixtures for apiV2
"""
import pytest
import psycopg2

from api_v2 import create_app

@pytest.fixture(scope='module')
def test_client():
    """
    Flask testclient setup
    """
    app = create_app('testing')
    app_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield app_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    """
    Create a test user
    """

    sql = """INSERT INTO users(first_name, last_name, email, password) VALUES
             ('John', 'Snow', 'snow@mail.com', 'kingofnorth')"""
    conn = None
    try:
    
        conn = psycopg2.connect(dbname='testdb', host='localhost',
                                user='testuser', password='testuser')

        cur = conn.cursor()

        #Create test user
        cur.execute(sql)

        cur.close()

        conn.commit()

    except (Exception , psycopg2.DatabaseError) as Error:
        print(Error)
    finally:
        if conn is not None:
            conn.close()
