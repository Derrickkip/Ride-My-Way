"""
Create db tables
"""
import psycopg2

COMMANDS = (
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL primary key,
        first_name varchar(80) not null,
        last_name varchar(80) not null,
        email varchar(80) not null,
        phone_number varchar(80) not null,
        password varchar (255) not null
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cars (
        car_id SERIAL primary key,
        car_model varchar(80) not null,
        registration varchar(80) not null unique,
        user_id int null references users(user_id),
        seats int not null
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS rides (
            ride_id SERIAL primary key,
            user_id int not null references users(user_id) on delete cascade,
            origin varchar(80) not null,
            destination varchar(80) not null,
            date_of_ride varchar(80) not null,
            time varchar(80) not null,
            price int not null,
            requests int default 0

    )
    """,
    """
    CREATE TABLE IF NOT EXISTS requests (
            request_id SERIAL primary key,
            user_id int references users(user_id) on delete cascade,
            ride_id int references rides(ride_id) on delete cascade,
            accept_status varchar(80) default 'pending'
    )
    """
)

def create_tables(db_url):
    """
    Create tables for the database
    """
    try:
        conn = psycopg2.connect(db_url)

        cur = conn.cursor()
        #create tables
        for command in COMMANDS:
            cur.execute(command)

        cur.close()

        conn.commit()

        conn.close()
    except psycopg2.DatabaseError as error:
        print(error)
