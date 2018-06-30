"""
Fixtures for apiV2
"""
import urllib.parse
import pytest
import psycopg2
import json

from api_v2 import create_app

result = urllib.parse.urlparse("postgresql://testuser:testuser@localhost/testdb")
username = result.username
database = result.path[1:]
hostname = result.hostname
dbpassword = result.password
 
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
        print('deleting data')
    
        conn = psycopg2.connect(database=database, user=username,
                                password=dbpassword, host=hostname)

        cur = conn.cursor()
        
        sqls = ('''DELETE FROM rides''', '''DELETE FROM requests''', '''DELETE FROM users''', )
        
        for sql in sqls:
            cur.execute(sql)

        cur.close()

        conn.commit()

        conn.close()

        ctx.pop()

    request.addfinalizer(fin)
