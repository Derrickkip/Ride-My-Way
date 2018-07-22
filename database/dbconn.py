"""
Database config
"""
import psycopg2
from flask import current_app

def dbconn():
    """
    return db connector
    """
    try:
        conn = psycopg2.connect(current_app.config['DATABASE'])

        return conn
    except psycopg2.DatabaseError as error:
        return {'error': str(error)}
