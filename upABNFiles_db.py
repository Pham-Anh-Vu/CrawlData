import datetime
import mariadb
from unidecode import unidecode
import connectdb

def upData(details, result):
    id = details[33][0]

    record = []
    for i in details[35]:
        bidform = i[4]
        link = f"https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode={bidform}&id={id}"
        filename = i[3]
        object_type = "App\Models\BiddingNewsDetail"
        object_id = result

        if filename == "Quyết định phê duyệt":
            tuples = (object_type, object_id, filename, link, 1)
            record.append(tuples)
        else:
            tuples = (object_type, object_id, filename, link, None)
            record.append(tuples)
    conn = connectdb.connect()
    mycursor = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news_files(object_type, object_id, file_name, link_muasamcong, created_at, updated_at, is_big_file) " \
              f"VALUES (%s, %s, %s, %s, '{datetime.datetime.now()}', '{datetime.datetime.now()}', %s);"
    mycursor.executemany(sql, record)
    conn.commit()