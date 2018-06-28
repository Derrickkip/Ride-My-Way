"""
Database setup
"""

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
            carmodel varchar(80) null
        )
        """,
        """ CREATE TABLE requests (
                request_id SERIAL primary key,
                user_id int references users(user_id)
        )
        """,
        """ CREATE TABLE rides (
                ride_id SERIAL primary key,
                user_id int not null references users(user_id),
                origin varchar(80) not null,
                destination varchar(80) not null,
                date_of_ride varchar(80) not null,
                time varchar(80) not null,
                price int not null,
                requests int null references requests(request_id)

        )
        """
    )
    
    conn = None
    
    try:
        conn = psycopg2.connect(dbname='testdb', host='localhost',
                            user='testuser', password='testuser')
        
        cur = conn.cursor()
        #create tables
        for command in commands:
            cur.execute(command)

        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as Error:
        print(Error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
