import mysql.connector
from mysql.connector import Error

def connect_database():
    db_name = 'librarymanagement'
    user = 'root'
    password = 'Tuckerstriker12'
    host = '127.0.0.1'

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host

        )
        
        if conn.is_connected():
            print("Connected to MySQL Database successfully")
            return conn

    except Error as e:
        print(f'An error has occured:{e}')


