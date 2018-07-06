"""
Create db tables
"""
import os
import psycopg2

def create_tables():
    """
    Create tables for the database
    """

    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL primary key,
            first_name varchar(80) not null,
            last_name varchar(80) not null,
            email varchar(80) not null,
            driving_licence varchar(80) null,
            carmodel varchar(80) null,
            password varchar (255) not null
        )
        """,
        """ CREATE TABLE rides (
                ride_id SERIAL primary key,
                user_id int not null references users(user_id) on delete cascade,
                origin varchar(80) not null,
                destination varchar(80) not null,
                date_of_ride varchar(80) not null,
                time varchar(80) not null,
                price int not null

        )
        """,
        """ CREATE TABLE requests (
                request_id SERIAL primary key,
                user_id int references users(user_id) on delete cascade,
                ride_id int references rides(ride_id) on delete cascade,
                accept_status varchar(80) default 'pending'
        )
        """
    )

    try:
        conn = psycopg2.connect(os.getenv('DATABASE'))

        cur = conn.cursor()
        #create tables
        for command in commands:
            cur.execute(command)

        cur.close()

        conn.commit()

        conn.close()
    except psycopg2.DatabaseError as error:
        print(error)


if __name__ == '__main__':
    create_tables()
