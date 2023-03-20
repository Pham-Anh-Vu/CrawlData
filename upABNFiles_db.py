import datetime
import mariadb
from unidecode import unidecode
import connectdb
import upFileDinhKemHSMT

def upData(details, result, link1):
    id1 = details[33][0]
    object_type = 'App\Models\BiddingNewsDetail'
    object_id = int(result)
    record = []
    media_id = None
    record.append([object_type, object_id, 'Quyết định phê duyệt', link1 ,media_id, 1])
    for i in details[35]:
        bidform = i[4]
        link = f"https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode={bidform}&id={id1}"
        filename = i[3]
        if filename == "Quyết định phê duyệt":
            tuples = (object_type, object_id, filename, link, media_id, 1)
            record.append(tuples)
        else:
            tuples = (object_type, object_id, filename, link, media_id, None)
            record.append(tuples)
        for z in details[37]:
            if i[5] == z[2]:
                if z[1] == i[4]:
                    media_id1, filename1, link2 = up_pccc_app_medias(code=z[0])
                    tuples = (object_type, object_id, filename1, link2, media_id1, None)
                    record.append(tuples)
                else:
                    if z[2] == 'P2':
                        media_id1, filename1, link2 = up_pccc_app_medias(code=z[0])
                        tuples = (object_type, object_id, filename1, link2, media_id1, None)
                        record.append(tuples)
            else:
                if z[2]=='C8':
                    if i[4] == 'C8':
                        media_id1, filename1, link2 = up_pccc_app_medias(code=z[0])
                        tuples = (object_type, object_id, filename1, link2, media_id1, None)
                        record.append(tuples)
            
    conn = connectdb.connect()
    cur = conn.cursor()
    for recordx in record:
        sql = "INSERT INTO pccc_app_bidding_news_files (object_type, object_id, file_name, link_muasamcong, media_id, created_at, updated_at, is_big_file) VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s);"
        cur.execute(sql, recordx)
        conn.commit()


def up_pccc_app_medias(code):
    url = 'http://localhost:1234/api/download/file/browser/public?fileId='+code
    name,type,path, file_name_for_user = upFileDinhKemHSMT.downFileAndUpLoad(url=url)
    conn = connectdb.connect()
    cur = conn.cursor()
    sql= "INSERT INTO pccc_app_medias (name, type, path, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())"
    val = (name, type, path)
    cur.execute(sql,val)
    conn.commit()
    media_id = cur.lastrowid
    media_id = int(media_id)
    return media_id, file_name_for_user, url
                    



