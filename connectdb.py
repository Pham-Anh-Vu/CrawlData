# import mariadb
import sys

# import mariadb as mariadb
import mariadb
import mysql.connector
def connect():
    try:
        #conn = mysql.connector.connect(user="tindauthau",password="X9G[uJ2T/lVvWm*t",host="db.rsa.vn",port=3308,database="krongpa")


        conn = mysql.connector.connect(user="root",password="Nmd021200.",host="127.0.0.1",port=3309,database="test")
        return conn
    
    except mysql.connector.Error as e:
        print(f"Error connecting: {e}")
        sys.exit(1)
