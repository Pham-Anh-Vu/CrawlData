import datetime
from datetime import datetime
import connectdb

def time(data):
    time = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
    time = datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    return time

def upData(details, news_id, result):
    for i in details[36]:
        if len(i) == 5 and i[4] != '00' and i[4] != 0:
            contractor_name = i[1]
            conn = connectdb.connect()
            cur = conn.cursor()
            sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
            val = (contractor_name,)
            cur.execute(sql, val)
            a = cur.fetchone()
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
            continue

# details = ['IB2300047604',
#            '2023-03-23T11:08:38.406',
#            '00',
#            'PL2300036765',
#            'Chi thường xuyên',
#            "Thu gom rác, vận chuyển rác thải sinh hoạt đến điểm tập kết và xử lý rác tạm thời trên địa bàn xã Bàn Giản ( từ ngày 01/04/2023 đến ngày 31/12/2023)",
#            "Thu gom rác, vận chuyển rác thải sinh hoạt đến điểm tập kết và xử lý rác tạm thời trên địa bàn xã Bàn Giản ( từ ngày 01/04/2023 đến ngày 31/12/2023)",
#            "UBND xã Bàn Giản, huyện Lập Thạch",
#            "UBND xã Bàn Giản, huyện Lập Thạch",
#            'Nguồn vốn sự nghiệp môi trường và các nguồn huy động hợp pháp khác',
#            'Phi tư vấn',
#            'Chào hàng cạnh tranh',
#            'TG',
#            'Trong nước',
#            'Một giai đoạn một túi hồ sơ',
#            '272D',
#            'Qua mạng',
#            'https://muasamcong.mpi.gov.vn',
#            "220,000 VND",
#            'https://muasamcong.mpi.gov.vn',
#            "Huyện Lập Thạch, Tỉnh Vĩnh Phúc",
#            '2023-03-30T07:30:00',
#            '2023-03-30T07:30:00',
#            'https://muasamcong.mpi.gov.vn',
#            '60D',
#            5000000,
#            352052000,
#            'Cam kết',
#            '40/QĐ-UBND',
#            '2023-03-15T17:00:00.000+0000',
#            'UBND xã Bàn Giản',
#            "('http://localhost:1234/api/download/file/browser/public?fileId=a51c75e6-4f32-489a-ae1b-a0501eb40e62',)",
#            "('https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=effad1d2-0857-4ac9-8db5-38f2282c0394',)",
#            1,
#            '2023-03-30T07:40:52',
#            "[['vn2500667324', 'HỢP TÁC XÃ DỊCH VỤ TỔNG HỢP BÀN GIẢN', 351164000, 0, 351164000, 60, 5000000, 90, '272D']]",
#            "[['vn2500667324', 'HỢP TÁC XÃ DỊCH VỤ TỔNG HỢP BÀN GIẢN', 351164000, 351164000, '272D']]",
#            "['effad1d2-0857-4ac9-8db5-38f2282c0394', 'IB2300047604', 'es-notify-contractor', 'notify-contractor-step-4-kqlcnt', 'CNTTT', 'ba7b1d27-657e-43f1-9589-20b73cb68cf1', 1, 'PTV', '00']",
#            '2023-03-31T23:59:59',
#            [None],
#            []]
#
# upData(details, 1841085, 1)