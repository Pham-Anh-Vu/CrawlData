import datetime

import mariadb
from unidecode import unidecode
import connectdb

def time_close(data):
    time = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
    time = datetime.datetime.strftime(time, '%d/%m/%Y %H:%M')
    return time

def time_post(data):
    tim_post = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
    tim_post = datetime.datetime.strftime(tim_post, '%Y-%m-%d %H:%M:%S')
    return tim_post

def upData(details, id1):
    titles1 = 'Hình thức thông báo'

    titles2 = 'Loại thông báo'

    titles3 = 'Số TBMT'

    titles4 = 'Thời điểm đăng tải'

    titles5 = 'Số hiệu KHLCNT'

    titles6 = 'Tên KHLCNT'

    titles7 = 'Lĩnh vực'

    titles8 = 'Bên mời thầu'

    titles9 = 'Tên gói thầu'

    titles10 = 'Phân loại'

    titles11 = 'Tên dự toán mua sắm'

    titles12 = 'chi tiết nguồn vốn'

    titles13 = 'Loại hợp đồng'

    titles14 = 'Hình thức lựa chọn nhà thầu'

    titles15 = 'Phương thức LCNT'

    titles16 = 'Thời gian thực hiện hợp đồng'

    titles17 = 'Hình thức dự thầu'

    titles18 = 'Thời gian nhận E-HSDT từ ngày'

    titles19 = 'Đến ngày'

    titles20 = 'Phát hành E-HSMT'

    titles21 = 'Thời gian hiệu lực của E-HSDT'

    titles22 = 'Địa điểm nhận E-HSMT'

    titles23 = 'Địa điểm thực hiện gói thầu'

    titles24 = 'Thời gian đóng/mở thầu'

    titles25 = 'Địa điểm mở thầu'

    titles26 = 'Dự toán gói thầu'

    titles27 = 'Số tiền bảo đảm dự thầu'

    titles28 = 'Hình thức bảo đảm dự thầu'

    titles29 = 'Hồ sơ mời thầu'

    titles30 = 'Làm rõ E-HSMT'

    titles31 = 'Hội nghị tiền đấu thầu'

    key1 = titles1.strip().lower().replace(' ', '-')
    key1 = unidecode(key1)

    key2 = titles2.strip().lower().replace(' ', '-')
    key2 = unidecode(key2)

    key3 = titles3.strip().lower().replace(' ', '-')
    key3 = unidecode(key3)

    key4 = titles4.strip().lower().replace(' ', '-')
    key4 = unidecode(key4)

    key5 = titles5.strip().lower().replace(' ', '-')
    key5 = unidecode(key5)

    key6 = titles6.strip().lower().replace(' ', '-')
    key6 = unidecode(key6)

    key7 = titles7.strip().lower().replace(' ', '-')
    key7 = unidecode(key7)

    key8=titles8.strip().lower().replace(' ', '-')
    key8 = unidecode(key8)

    key9 = titles9.strip().lower().replace(' ', '-')
    key9 = unidecode(key9)

    key10 = titles10.strip().lower().replace(' ', '-')
    key10 = unidecode(key10)

    key11 = titles11.strip().lower().replace(' ', '-')
    key11 = unidecode(key11)

    key12 = titles12.strip().lower().replace(' ', '-')
    key12 = unidecode(key12)

    key13 = titles13.strip().lower().replace(' ', '-')
    key13 = unidecode(key13)

    key14 = titles14.strip().lower().replace(' ', '-')
    key14 = unidecode(key14)

    key15 = titles15.strip().lower().replace(' ', '-')
    key15 = unidecode(key15)

    key16 = titles16.strip().lower().replace(' ', '-')
    key16 = unidecode(key16)

    key17 = titles17.strip().lower().replace(' ', '-')
    key17 = unidecode(key17)

    key18 = titles18.strip().lower().replace(' ', '-')
    key18 = unidecode(key18)

    key19 = titles19.strip().lower().replace(' ', '-')
    key19 = unidecode(key19)

    key20 = titles20.strip().lower().replace(' ', '-')
    key20 = unidecode(key20)

    key21 = titles21.strip().lower().replace(' ', '-')
    key21 = unidecode(key21)

    key22 = titles22.strip().lower().replace(' ', '-')
    key22 = unidecode(key22)

    key23 = titles23.strip().lower().replace(' ', '-')
    key23 = unidecode(key23)

    key24 = titles24.strip().lower().replace(' ', '-')
    key24 = unidecode(key24)

    key25 = titles25.strip().lower().replace(' ', '-')
    key25 = unidecode(key25)

    key26 = titles26.strip().lower().replace(' ', '-')
    key26 = unidecode(key26)

    key27 = titles27.strip().lower().replace(' ', '-')
    key27 = unidecode(key27)

    key28 = titles28.strip().lower().replace(' ', '-')
    key28 = unidecode(key28)

    key29 = titles29.strip().lower().replace(' ', '-')
    key29 = unidecode(key29)

    key30 = titles30.strip().lower().replace(' ', '-')
    key30 = unidecode(key30)

    key31 = titles31.strip().lower().replace(' ', '-')
    key31 = unidecode(key31)

    sub_title1 = "Thông tin liên quan đến đấu thầu"
    sub_title2 = "Thông tin liên quan đến đấu thầu"
    sub_title3 = "Thông tin chung"
    sub_title4 = "Thông tin chung"
    sub_title5 = "Thông tin chung"
    sub_title6 = "Thông tin chung"
    sub_title7 = "Thông tin chung"
    sub_title8 = "Thông tin chung"
    sub_title9 = "Thông tin chung"
    sub_title10 = "Thông tin chung"
    sub_title11 = "Thông tin chung"
    sub_title12 = "Thông tin chung"
    sub_title13 = "Thông tin chung"
    sub_title14 = "Thông tin chung"
    sub_title15 = "Thông tin chung"
    sub_title16= "Thông tin chung"
    sub_title17 = "Tham dự thầu"
    sub_title18 = "Tham dự thầu"
    sub_title19 = "Tham dự thầu"
    sub_title20 = "Tham dự thầu"
    sub_title21 = "Tham dự thầu"
    sub_title22 = "Tham dự thầu"
    sub_title23 = "Tham dự thầu"
    sub_title24 = "Mở thầu"
    sub_title25 = "Mở thầu"
    sub_title26 = "Mở thầu"
    sub_title27 = "Bảo đảm dự thầu"
    sub_title28 = "Bảo đảm dự thầu"
    sub_title29 = "Bảo đảm dự thầu"
    sub_title30 = "Bảo đảm dự thầu"
    sub_title31 = "Bảo đảm dự thầu"

    if details[2] != "00" or details[2] != 00:
        value1 = "Điều chỉnh"
    else: 
        value1 = "Đăng lần đầu"

    value2 = "Thông báo thực"

    value3 = f"{details[0]} - {details[2]}"

    value4 = time_post(details[1])

    value5 = details[3]

    value6 = details[5]

    value7 = details[10]

    value8 = details[7]

    value9 = details[6]

    value10 = details[4]

    value11 = details[5]

    value12 = details[9]

    if details[12] == "TG":
        value13 = "Trọn Gói"
    else: 
        value13 = ""
    value14 = f"{details[11]} {details[13]}"

    value15 = details[14]

    for i in details[15]:
        if i.isnumeric(): continue
        else:
            if i == "D":
                value16 = details[15].replace("D", " Ngày")
            elif i == "M":
                value16 = details[15].replace("M", " tháng")

    value17 = f"Đấu thầu {details[16].lower()}"

    value18 = time_post(details[1])

    value19 = time_close(details[21])

    if details[18] == '' or details[18] == 0 :
        value20 = 'Miễn phí'
    else:
        value20 = details[18]
    
    for i in details[24]:
        if i.isnumeric(): continue
        else:
            if i == "D":
                value21 = details[24].replace("D", " Ngày")
            elif i == "M":
                value21 = details[24].replace("M", " tháng")

    value22 = details[19]

    value23 = details[20]

    value24 = value19

    value25 = details[23]

    if details[26] != '':
        value26 = int(details[26])
        value26 = "{:,}".format(value26).replace(",", ".") + " VND"
    else:
        value26 = details[26]

    if details[25] != '':
        value27 = int(details[25])
        value27 = "{:,}".format(value27).replace(",", ".") + " VND"
    else:
        value27 = details[25]

    value28 = details[27]

    value29 = None
    value30 = None
    value31 = None

    conn = connectdb.connect()
    cur = conn.cursor()
    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value8,)
    cur.execute(sql,val)
    conn.commit()
    myresult = cur.fetchone()

    if myresult is not None:
        if myresult != []:
            subject_id_1 = myresult[0]
            subject_id_1 = str(subject_id_1)
            subject_type_1 = 'App\Models\JobCompanyProfile'
    else:
        subject_id_1 = None
        subject_type_1 = None

    records = [
        (key1, sub_title1, titles1, value1, id1),
        (key2, sub_title2, titles2, value2, id1),
        (key3, sub_title3, titles3, value3, id1),
        (key4, sub_title4, titles4, value4, id1),
        (key5, sub_title5, titles5, value5, id1),
        (key6, sub_title6, titles6, value6, id1),
        (key7, sub_title7, titles7, value7, id1),
        (key8, sub_title8, titles8, value8, id1),
        (key9, sub_title9, titles9, value9, id1),
        (key10, sub_title10, titles10, value10, id1),
        (key11, sub_title11, titles11, value11, id1),
        (key12, sub_title12, titles12, value12, id1),
        (key13, sub_title13, titles13, value13, id1),
        (key14, sub_title14, titles14, value14, id1),
        (key15, sub_title15, titles15, value15, id1),
        (key16, sub_title16, titles16, value16, id1),
        (key17, sub_title17, titles17, value17, id1),
        (key18, sub_title18, titles18, value18, id1),
        (key19, sub_title19, titles19, value19, id1),
        (key20, sub_title20, titles20, value20, id1),
        (key21, sub_title21, titles21, value21, id1),
        (key22, sub_title22, titles22, value22, id1),
        (key23, sub_title23, titles23, value23, id1),
        (key24, sub_title24, titles24, value24, id1),
        (key25, sub_title25, titles25, value25, id1),
        (key26, sub_title26, titles26, value26, id1),
        (key27, sub_title27, titles27, value27, id1),
        (key28, sub_title28, titles28, value28, id1),
        (key29, sub_title29, titles29, value29, id1),
        (key30, sub_title30, titles30, value30, id1),
        (key31, sub_title31, titles31, value31, id1)]

    sql = "INSERT INTO pccc_app_bidding_news_details(`key`, sub_title, title, value, news_id, type_id, created_at, updated_at) " \
          f"VALUES (%s, %s, %s, %s, %s, 3, NOW(), NOW());"
    cur.executemany(sql, records)
    conn.commit()