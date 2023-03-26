import datetime
from datetime import datetime
import connectdb

def time(data):
    time = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
    time = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    return time


def upDataDB(details, news_id):
    for company in details[33]:
        contractor_name = str(company[1])
        bid_price = str(company[2])
        dis_rate = str(company[3])
        bid_price_after_dis = str(company[4])
        e_hsdxtc = str(company[5])
        value_bd_tt = str(company[6])
        e_bd_dt = str(company[7])
        duration_contract = ''
        for i in company[8]:
            if i.isdecimal():
                continue
            else:
                if i == "D":
                    duration_contract = company[8].replace("D", " ngày")
                elif i == "M":
                    duration_contract = company[8].replace("M", " tháng")
        subject_type = "App\Models\JobCompanyProfile"

        conn = connectdb.connect()
        cur = conn.cursor()
        sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
        val = (contractor_name,)
        cur.execute(sql, val)
        conn.commit()
        cur.fetchone()
        number_dkkd = ""
        subject_id = ""

        if cur.fetchone() != None:
            for i in cur.fetchone():
                number_dkkd = str(cur.fetchone()[15])
                subject_id = str(cur.fetchone()[0])
        # vì data test chưa có app job company profile nên subject id đặt bằng 0
        data = (news_id, number_dkkd, contractor_name, bid_price, dis_rate, bid_price_after_dis, e_hsdxtc, value_bd_tt, e_bd_dt, duration_contract, time(str(datetime.now())), time(str(datetime.now())), 0,subject_type, )
        sql = "INSERT INTO pccc_app_bidding_open_result_bid_open_complete(news_id, number_dkkd, contractor_name, bid_price, discount_rate, bid_price_after_discount, effect_hsdxtc, value_bd_dt, effect_bd_dt, duration_of_contract, created_at, updated_at, subject_id, subject_type)" \
              f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, data)
        conn.commit()
