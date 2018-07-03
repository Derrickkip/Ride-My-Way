"""
Database config
"""

import psycopg2
from flask import current_app

def dbconn():
    """
    return db connector
    """
    conn = psycopg2.connect(current_app.config['DATABASE'])

    return conn


