import datetime
from datetime import datetime
import connectdb

def time(data):
    time = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
    time = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    return time

def upData(details, news_id, result):
    print(details[36])
    for i in details[36]:
        print(i)
        if len(i) == 5 and i[4] != '00' and i[4] != 0:
            contractor_name = i[1]
            conn = connectdb.connect()
            cur = conn.cursor()
            sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
            val = (contractor_name,)
            cur.execute(sql, val)
            a = cur.fetchone()
            conn.commit()
            number_dkkd = ""
            subject_id = 0
            if cur.fetchone() != None:
                for i in cur.fetchone():
                    number_dkkd = str(a[15])
                    subject_id = str(a[0])
            bid_price = str('{:,}'.format(int(i[2])).replace(',', '.')) + 'VND'
            dis_rate = ((int(i[2]) - int(i[3]))/int(i[2]))*100
            bid_price_after_dis = str('{:,}'.format(int(i[2])).replace(',', '.'))+ 'VND'
            subject_type = "App\Models\JobCompanyProfile"
            data = (news_id, 0, number_dkkd, contractor_name, bid_price, dis_rate, bid_price_after_dis, time(str(datetime.now())), time(str(datetime.now())), subject_id, subject_type, result)
            sql = "INSERT INTO pccc_app_bidding_open_result_complete_gd_hsdt(news_id, ratings, number_dkkd, contractor_name, bid_price, discount_rate, bid_price_after_discount, created_at, updated_at, subject_id, subject_type, result)" \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql, data)
            conn.commit()
        else:
            print("details")
            continue
