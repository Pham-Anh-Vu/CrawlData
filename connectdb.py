# import mariadb
import sys

# import mariadb as mariadb
import mariadb
import mysql.connector
def connect():

    try:
        conn = mariadb.connect(
            user="root",
            password="123123",
            host="127.0.0.1",
            port=3306,
            database="test"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
