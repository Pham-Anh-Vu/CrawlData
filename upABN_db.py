import json
import mariadb
import datetime

def connect():
    conn = mariadb.connect(
        user="root",
        password="123123",
        host="127.0.0.1",
        port=3306,
        database="abc"
    )
    return conn

def upDataDB(type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no, time_bid_closing, time_posting, date_of_approval):
    conn = connect()
    mycursor = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news (type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no, time_bid_closing, time_posting, date_of_approval,is_related) " \
          f"VALUES ('{type_id}', '{bid_type}', '{bid_method}', '{aujusted_limited}', '{created_at}','{updated_at}', '{bid_number}', '{bid_turn_no}', '{time_bid_closing}', '{time_posting}', '{date_of_approval}')"
    mycursor.execute(sql)
    conn.commit()

def yesterday():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.date()
    yesterday = yesterday.strftime('%Y-%m-%d')
    return yesterday

def data():
    data = []
    datas = []
    with open(f"{yesterday()}to{yesterday()}\TBMT_CDT.csv", encoding="utf8") as file:
        data1 = file.readlines()
        for i in data1:
            if i == "\n":
                continue
            data.append(i)
    for i in data:
        i = i.split(",")
        datas.append(i)

    # kt data
    details = []
    for data in datas:
        try:
            if len(data[2]) == 2 :
                details.append(data)
        except IndexError:
            continue
    return details

# kt = 0
# details = data()
# for data in details[0]:
#     print(f"{kt} -- {data}")
#     kt += 1


kt = 0
details = data()
print(details[4])
# for data in details:
#     print(data[29])
#     if len(data) < 20:
#         continue
#     if data[10] == "Hàng hóa":
#         bid_type = 0
#     if data[10] == "Xây lắp":
#         bid_type = 1
#     if data[10] == "Phi tư vấn":
#         bid_type = 3
#     if data[10] == "Tư vấn":
#         bid_type = 2
#     else:
#         bid_type = 4
#
#     if data[16] == "Qua mạng":
#         bid_method = 1
#     else: bid_method = 0
#     #0: bid_number
#     #10 -- bid_type
#     #16 -- bid_me
#     #2 bid_turn_no
#     # 22, 23 closin op
#     # 1 posting
#     crea_at = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
#     upd_at = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
#     tim_clos = datetime.datetime.strptime(data[22], '%Y-%m-%dT%H:%M:%S')
#     tim_clos = datetime.datetime.strftime(tim_clos, '%Y-%m-%d %H:%M:%S')
#     tim_post = datetime.datetime.strptime(data[1], '%Y-%m-%dT%H:%M:%S.%f')
#     tim_post = datetime.datetime.strftime(tim_post, '%Y-%m-%d %H:%M:%S')
#     dat_app = datetime.datetime.strptime(data[29], '%d/%m/%Y')
#     dat_app = datetime.datetime.strftime(dat_app, '%Y%m-%d %H:%M:%S')
#     print(kt)
#     kt+=1

#
#     upDataDB(3, bid_type, bid_method, 1, crea_at, upd_at, data[0], data[2], tim_post, dat_app )
#     type_id, bid_type, bid_method, aujusted_limited, created_at, updated_at, bid_number, bid_turn_no, time_bid_closing, time_posting, date_of_approval

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
    if data == "Xây lắp":
        bid_type = 1
    if data == "Phi tư vấn":
        bid_type = 3
    if data == "Tư vấn":
        bid_type = 2
    else:
        bid_type = 4
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
    time = datetime.datetime.strftime(time, '%Y%m-%d %H:%M:%S')
    return time

def time_post(data):
    tim_post = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
    tim_post = datetime.datetime.strftime(tim_post, '%Y-%m-%d %H:%M:%S')
    return tim_post

def date_app(data):
    dat_app = datetime.datetime.strptime(data, '%d/%m/%Y')
    dat_app = datetime.datetime.strftime(dat_app, '%Y%m-%d %H:%M:%S')
    return dat_app