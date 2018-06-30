"""
Fixtures for apiV2
"""
import urllib.parse
import pytest
import psycopg2

from api_v2 import create_app

DB = urllib.parse.urlparse("postgresql://testuser:testuser@localhost/testdb")
USERNAME = DB.username
DATABASE = DB.path[1:]
HOSTNAME = DB.hostname
PASSWORD = DB.password

@pytest.fixture(scope='module')
def test_client(request):
    """
    Flask testclient setup
    """
    app = create_app('testing')
    app_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield app_client

    def fin():
        '''
        Function to be run at end of test
        '''
        print('deleting data')

        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                password=PASSWORD, host=HOSTNAME)

        cur = conn.cursor()

        sqls = ('''DELETE FROM requests''', '''DELETE FROM rides''',
                '''DELETE FROM users''', )

        for sql in sqls:
            cur.execute(sql)

        cur.close()

        conn.commit()

        conn.close()

        ctx.pop()

    request.addfinalizer(fin)
