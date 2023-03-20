import csv
import json
import mariadb
import datetime

def connect():
    conn = mariadb.connect(
        user="root",
        password="Nmd021200.",
        host="127.0.0.1",
        port=3306,
        database="test"
    )
    return conn

def ktTrungDL(id, turn_no):
    conn = connect()
    mycursor = conn.cursor()
    sql = f"SELECT * FROM pccc_app_bidding_news WHERE bid_number = '{id}' AND bid_turn_no = '{turn_no}'"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    return result

def bid_type(data):
    if data == "Hàng hóa":
        bid_type = 0
    elif data == "Xây lắp":
        bid_type = 1
    elif data == "Phi tư vấn":
        bid_type = 3
    elif data == "Tư vấn":
        bid_type = 2
    elif data == "Hỗn hợp":
        bid_type = 4
    else: bid_type = 5
    return bid_type

def bid_method(data):
    if data == "Qua mạng":
        bid_method = 1
    else:
        bid_method = 0
    return bid_method

def timeUpd():
    crea_at = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    return crea_at

def time_close(data):
    time = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    time = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    return time

def time_post(data):
    tim_post = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
    tim_post = datetime.datetime.strftime(tim_post, '%Y-%m-%d %H:%M:%S')
    return tim_post

def date_app(data):
    dat_app = datetime.datetime.strptime(data, '%d/%m/%Y')
    dat_app = datetime.datetime.strftime(dat_app, '%Y-%m-%d %H:%M:%S')
    return dat_app

def upDataDB(type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no, time_bid_closing, time_posting, date_of_approval):
    conn = connect()
    mycursor = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news (type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no, time_bid_closing, time_posting, date_of_approval) " \
          f"VALUES ('{type_id}', '{bid_type}', '{bid_method}', '{aujusted_limited}', '{created_at}','{updated_at}', '{bid_number}', '{bid_turn_no}', '{time_bid_closing}', '{time_posting}', '{date_of_approval}');"
    mycursor.execute(sql)
    conn.commit()
    news_id = mycursor.lastrowid
    news_id = int(news_id)
    return news_id
def yesterday():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.date()
    yesterday = yesterday.strftime('%Y-%m-%d')
    return yesterday

def upDataDB_DXT(bid_open_tim, news_id):
    conn = connect()
    mycursor = conn.cursor()
    sql = f"UPDATE pccc_app_bidding_news SET bid_opening_time = '{bid_open_tim}', open_result_status = 'bid_open_complete' WHERE `id` = '{news_id}';"
    mycursor.execute(sql)
    conn.commit()

def upDataDB_1_DXT(type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no):
    conn = connect()
    mycursor = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news (type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no) " \
          f"VALUES ('{type_id}', '{bid_type}', '{bid_method}', '{aujusted_limited}', '{created_at}','{updated_at}', '{bid_number}', '{bid_turn_no}');"
    mycursor.execute(sql)
    conn.commit()
    news_id = mycursor.lastrowid
    news_id = int(news_id)
    return news_id