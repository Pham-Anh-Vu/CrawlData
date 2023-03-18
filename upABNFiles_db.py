import datetime
import mariadb
from unidecode import unidecode
import connectdb

def upData(details, result, link1):
    id1 = details[33][0]
    object_type = 'App\Models\BiddingNewsDetail'
    object_id = int(result)
    record = []
    record.append([object_type, object_id, 'Quyết định phê duyệt', link1, 1])
    for i in details[35]:
        bidform = i[4]
        link = f"https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode={bidform}&id={id1}"
        filename = i[3]
        if filename == "Quyết định phê duyệt":
            tuples = (object_type, object_id, filename, link, 1)
            record.append(tuples)
        else:
            tuples = (object_type, object_id, filename, link, None)
            record.append(tuples)

    conn = connectdb.connect()
    cur = conn.cursor()
    for recordx in record:
        sql = "INSERT INTO pccc_app_bidding_news_files (object_type, object_id, file_name, link_muasamcong, created_at, updated_at, is_big_file) VALUES (%s, %s, %s, %s, NOW(), NOW(), %s);"
        cur.execute(sql, recordx)
        conn.commit()