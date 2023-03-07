import mariadb
import sys
def connect():
    try:
        conn = mariadb.connect(
            user="root",
            password="Nmd021200.",
            host="127.0.0.1",
            port=3306,
            database="test"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
