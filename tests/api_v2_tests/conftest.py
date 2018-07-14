"""
Fixtures for apiV2
"""
import os
import pytest
import psycopg2

from api_v2 import create_app


@pytest.fixture(scope='module')
def test_client(request):
    """
    Flask testclient setup
    """
    app = create_app('testing')
    app_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    dbase = os.getenv('TEST_DB')
    yield app_client

    def fin():
        '''
        Function to be run at end of test
        '''
        print('deleting data')

        conn = psycopg2.connect(dbase)

        cur = conn.cursor()

        sqls = ('''DELETE FROM cars''','''DELETE FROM requests''', '''DELETE FROM rides''',
                '''DELETE FROM users''', )

        for sql in sqls:
            cur.execute(sql)

        cur.close()

        conn.commit()

        conn.close()

        ctx.pop()

    request.addfinalizer(fin)
