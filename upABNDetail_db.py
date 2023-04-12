import datetime
import json

import mariadb
from unidecode import unidecode
import connectdb

def time_close(data):
    if data == '':
        return None
    else:
        data = data[:19]
        time = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
        time = datetime.datetime.strftime(time, '%d/%m/%Y %H:%M')
        return time

def time_post(data):
    if data == '':
        return None
    else:
        data = data[:19]
        tim_post = datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S')
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

def upData_DXT(details, id):
    title1 = "Số TBMT"
    title2 = "Mua Hồ sơ mời thầu"
    title3 = "Tên gói thầu"
    title4 = "Chủ đầu tư"
    title5 = "Hình thức hợp đồng"
    title6 = "Bên mời thầu"
    title7 = "Hình thức lựa chọn nhà thầu"
    title8 = "Giá gói thầu"
    title9 = "Thời điểm hoàn thành"
    title10 = "Trạng thái gói thầu"
    title11 = "Số lượng nhà thầu"
    sub_title = "Thông tin chi tiết"

    key1 = title1.strip().lower().replace(' ', '-')
    key1 = unidecode(key1)

    key2 = title2.strip().lower().replace(' ', '-')
    key2 = unidecode(key2)

    key3 = title3.strip().lower().replace(' ', '-')
    key3 = unidecode(key3)

    key4 = title4.strip().lower().replace(' ', '-')
    key4 = unidecode(key4)

    key5 = title5.strip().lower().replace(' ', '-')
    key5 = unidecode(key5)

    key6 = title6.strip().lower().replace(' ', '-')
    key6 = unidecode(key6)

    key7 = title7.strip().lower().replace(' ', '-')
    key7 = unidecode(key7)

    key8 = title8.strip().lower().replace(' ', '-')
    key8 = unidecode(key8)

    key9 = title9.strip().lower().replace(' ', '-')
    key9 = unidecode(key9)

    key10 = title10.strip().lower().replace(' ', '-')
    key10 = unidecode(key10)

    key11 = title11.strip().lower().replace(' ', '-')
    key11 = unidecode(key11)

    value1 = f"{details[0]} - {details[2]}"

    value2 = details[18]

    value3 = details[6]

    value4 = details[7]

    if details[12] == "TG":
        value5 = "Trọn Gói"
    else:
        value5 = ""

    value6 = details[7]

    value7 = details[11]

    value8 = str(details[30])

    value9 = time_close(details[34])

    value10 = "Hoàn thành mở thầu"

    value11 = str(details[31])

    records = [
        (key1, sub_title, title1, value1, id),
        (key2, sub_title, title2, value2, id),
        (key3, sub_title, title3, value3, id),
        (key4, sub_title, title4, value4, id),
        (key5, sub_title, title5, value5, id),
        (key6, sub_title, title6, value6, id),
        (key7, sub_title, title7, value7, id),
        (key8, sub_title, title8, value8, id),
        (key9, sub_title, title9, value9, id),
        (key10, sub_title, title10, value10, id),
        (key11, sub_title, title11, value11, id)]
    conn = connectdb.connect()
    cur = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news_details(`key`, sub_title, title, value, news_id, type_id, created_at, updated_at) " \
          f"VALUES (%s, %s, %s, %s, %s, 7, NOW(), NOW());"
    cur.executemany(sql, records)
    conn.commit()


    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value4,)
    cur.execute(sql, val)
    conn.commit()
    cur.fetchone()
    if cur.fetchone() is None:
        myresult = ""
    else:
        myresult = cur.fetchone()[0]

    if myresult != "":
        sql = f"UPDATE pccc_app_bidding_news_details SET subject_id = '{myresult}', subject_type = 'App\Models\JobCompanyProfile' WHERE `title` = 'Chủ đầu tư' AND news_id = '{id}';"
        cur.execute(sql)
        conn.commit()

    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value6,)
    cur.execute(sql, val)
    conn.commit()
    cur.fetchone()
    if cur.fetchone() is None:
        myresult = ""
    else: myresult = cur.fetchone()[0]

    if myresult != "":
        sql = f"UPDATE pccc_app_bidding_news_details SET subject_id = '{myresult}', subject_type = 'App\Models\JobCompanyProfile' WHERE `title` = 'Bên mời thầu' AND news_id = '{id}';"
        cur.execute(sql)
        conn.commit()


def upData_DXT_TV(details, id):
    title1 = "Số TBMT"
    title2 = "Mua Hồ sơ mời thầu"
    title3 = "Tên gói thầu"
    title4 = 'Loại hợp đồng'
    title5 = "Tên bên mời thầu"
    title6 = 'Phương thức'
    title7 = "Hình thức lựa chọn nhà thầu"
    title8 = "Tổng số NT nộp E-HSĐXKT"
    title9 = "Trạng thái gói thầu"
    title10 = 'Thời điểm hoàn thành'
    title11 = "Đánh giá về kỹ thuật"
    title12 = 'Đánh giá về giá'
    sub_title = "Thông tin chi tiết"

    key1 = title1.strip().lower().replace(' ', '-')
    key1 = unidecode(key1)

    key2 = title2.strip().lower().replace(' ', '-')
    key2 = unidecode(key2)

    key3 = title3.strip().lower().replace(' ', '-')
    key3 = unidecode(key3)

    key4 = title4.strip().lower().replace(' ', '-')
    key4 = unidecode(key4)

    key5 = title5.strip().lower().replace(' ', '-')
    key5 = unidecode(key5)

    key6 = title6.strip().lower().replace(' ', '-')
    key6 = unidecode(key6)

    key7 = title7.strip().lower().replace(' ', '-')
    key7 = unidecode(key7)

    key8 = title8.strip().lower().replace(' ', '-')
    key8 = unidecode(key8)

    key9 = title9.strip().lower().replace(' ', '-')
    key9 = unidecode(key9)

    key10 = title10.strip().lower().replace(' ', '-')
    key10 = unidecode(key10)

    key11 = title11.strip().lower().replace(' ', '-')
    key11 = unidecode(key11)

    key12 = title11.strip().lower().replace(' ', '-')
    key12 = unidecode(key11)

    value1 = f"{details[0]} - {details[2]}"

    value2 = details[18]

    value3 = details[6]

    if details[12] == "TG":
        value4 = "Trọn Gói"
    elif details[12] == 'TG_DGCD':
        value4 = 'Trọn gói và Theo đơn giá cố định'
    else:
        value4 = ""
    
    value5 = details[7]

    if details[14] == 'DTRR':
        value6 = 'Đấu thầu rộng rãi'
    else:
        value6 = details[14]

    value7 = details[11]
    
    value8 = str(details[31])

    value9 = "Hoàn thành mở đề xuất kỹ thuật"
    
    value10 = time_close(details[34])

    value11 = 'Đạt - Không đạt'

    value12 = 'Phương pháp giá thấp nhất'

    records = [
        (key1, sub_title, title1, value1, id),
        (key2, sub_title, title2, value2, id),
        (key3, sub_title, title3, value3, id),
        (key4, sub_title, title4, value4, id),
        (key5, sub_title, title5, value5, id),
        (key6, sub_title, title6, value6, id),
        (key7, sub_title, title7, value7, id),
        (key8, sub_title, title8, value8, id),
        (key9, sub_title, title9, value9, id),
        (key10, sub_title, title10, value10, id),
        (key11, sub_title, title11, value11, id),
        (key12, sub_title, title12, value12, id)]
    
    conn = connectdb.connect()
    cur = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news_details(`key`, sub_title, title, value, news_id, type_id, created_at, updated_at) " \
          f"VALUES (%s, %s, %s, %s, %s, 7, NOW(), NOW());"
    cur.executemany(sql, records)
    conn.commit()


    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value4,)
    cur.execute(sql, val)
    conn.commit()
    cur.fetchone()
    if cur.fetchone() is None:
        myresult = ""
    else:
        myresult = cur.fetchone()[0]

    if myresult != "":
        sql = f"UPDATE pccc_app_bidding_news_details SET subject_id = '{myresult}', subject_type = 'App\Models\JobCompanyProfile' WHERE `title` = 'Tên bên mời thầu' AND news_id = '{id}';"
        cur.execute(sql)
        conn.commit()


def upData_CNTTT(details, id1):
    titles1 = 'Số TBMT'

    titles2 = 'Chủ đầu tư'

    titles3 = 'Hình thức đấu thầu'

    titles4 = 'Hình thức dự thầu'

    titles5 = 'Tên gói thầu'

    titles6 = 'Giá gói thầu'

    titles7 = 'Giá dự toán'

    titles8 = 'Thời điểm hoàn thành'

    titles9 = 'Thời điểm đăng tải TBMT'

    titles10 = 'Tên nhà thầu'

    titles11 = 'Số ĐKKD'

    titles12 = 'Giá dự thầu (VND)'

    titles13 = 'Tỷ lệ giảm giá (%)'

    titles14 = 'Điểm kỹ thuật'

    titles15 = 'Giá đánh giá'

    titles16 = 'Giá dự thầu sau giảm giá (không tính các khoản tạm tính và dự phòng nếu có) (VND)'

    titles17 = 'Giá trúng thầu'

    titles18 = 'Thời gian thực hiện hợp đồng'

    titles19 = 'Ngày phê duyệt'

    titles20 = 'Báo cáo tổng hợp đánh giá E-HSDT và phê duyệt danh sách xếp hạng nhà thầu'

    titles21 = 'Quyết định phê duyệt kết quả đấu thầu'

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

    key8 = titles8.strip().lower().replace(' ', '-')
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

    sub_title = 'Thông tin chi tiết'

    value1 = f"{details[0]}-{details[2]}"
    value2 = details[8]
    value3 = details[11]
    value4 = f"Đấu thầu {details[16].lower()}"
    value5 = details[6]
    value6 = str('{:,}'.format(int(details[26])).replace(',', '.')) + 'VND'
    value7 = value6
    value8 = ''
    value9 = time_post(details[1])
    # details[36] = eval(details[36])
    value10 = details[36][0][1]
    # details[35] = eval(details[35])
    conn = connectdb.connect()
    cur = conn.cursor()
    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value10,)
    cur.execute(sql, val)
    a = cur.fetchone()
    conn.commit()
    value11 = ''
    if a != None:
        value11 = str(a[15])

    for i in details[35]:
        if details[36][0][1] != i[1]:
            continue
        value12 = str('{:,}'.format(int(i[2])).replace(',', '.')) + 'VND'
        value13 = str((i[3]))
        value16 = str('{:,}'.format(int(i[4])).replace(',', '.')) + 'VND'
    value14 = ''
    value15 = ''
    value17 = str('{:,}'.format(int(details[36][0][3])).replace(',', '.')) + 'VND'
    value18 = ''
    value19 = details[38]
    value20 = ''
    value21 = ''

    records = [
        (key1, sub_title, titles1, value1, id1),
        (key2, sub_title, titles2, value2, id1),
        (key3, sub_title, titles3, value3, id1),
        (key4, sub_title, titles4, value4, id1),
        (key5, sub_title, titles5, value5, id1),
        (key6, sub_title, titles6, value6, id1),
        (key7, sub_title, titles7, value7, id1),
        (key8, sub_title, titles8, value8, id1),
        (key9, sub_title, titles9, value9, id1),
        (key10, sub_title, titles10, value10, id1),
        (key11, sub_title, titles11, value11, id1),
        (key12, sub_title, titles12, value12, id1),
        (key13, sub_title, titles13, value13, id1),
        (key14, sub_title, titles14, value14, id1),
        (key15, sub_title, titles15, value15, id1),
        (key16, sub_title, titles16, value16, id1),
        (key17, sub_title, titles17, value17, id1),
        (key18, sub_title, titles18, value18, id1),
        (key19, sub_title, titles19, value19, id1),
        (key20, sub_title, titles20, value20, id1),
        (key21, sub_title, titles21, value21, id1),
    ]
    sql = "INSERT INTO pccc_app_bidding_news_details(`key`, sub_title, title, value, news_id, type_id, created_at, updated_at) " \
          f"VALUES (%s, %s, %s, %s, %s, 8, NOW(), NOW());"
    cur.executemany(sql, records)
    conn.commit()

    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value10,)
    cur.execute(sql, val)
    a = cur.fetchone()
    conn.commit()
    if a is None:
        myresult = ""
    else:
        myresult = a[0]

    if myresult != "":
        sql = f"UPDATE pccc_app_bidding_news_details SET subject_id = '{myresult}', subject_type = 'App\Models\JobCompanyProfile' WHERE `title` = 'Chủ đầu tư' AND news_id = '{id}';"
        cur.execute(sql)
        conn.commit()


details = ['IB2300047604',
           '2023-03-23T11:08:38.406',
           '00',
           'PL2300036765',
           'Chi thường xuyên',
           "Thu gom rác, vận chuyển rác thải sinh hoạt đến điểm tập kết và xử lý rác tạm thời trên địa bàn xã Bàn Giản ( từ ngày 01/04/2023 đến ngày 31/12/2023)",
           "Thu gom rác, vận chuyển rác thải sinh hoạt đến điểm tập kết và xử lý rác tạm thời trên địa bàn xã Bàn Giản ( từ ngày 01/04/2023 đến ngày 31/12/2023)",
           "UBND xã Bàn Giản, huyện Lập Thạch",
           "UBND xã Bàn Giản, huyện Lập Thạch",
           'Nguồn vốn sự nghiệp môi trường và các nguồn huy động hợp pháp khác',
           'Phi tư vấn',
           'Chào hàng cạnh tranh',
           'TG',
           'Trong nước',
           'Một giai đoạn một túi hồ sơ',
           '272D',
           'Qua mạng',
           'https://muasamcong.mpi.gov.vn',
           "220,000 VND",
           'https://muasamcong.mpi.gov.vn',
           "Huyện Lập Thạch, Tỉnh Vĩnh Phúc",
           '2023-03-30T07:30:00',
           '2023-03-30T07:30:00',
           'https://muasamcong.mpi.gov.vn',
           '60D',
           5000000,
           352052000,
           'Cam kết',
           '40/QĐ-UBND',
           '2023-03-15T17:00:00.000+0000',
           'UBND xã Bàn Giản',
           "('http://localhost:1234/api/download/file/browser/public?fileId=a51c75e6-4f32-489a-ae1b-a0501eb40e62',)",
           "('https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=effad1d2-0857-4ac9-8db5-38f2282c0394',)",
           1,
           '2023-03-30T07:40:52',
           "[['vn2500667324', 'HỢP TÁC XÃ DỊCH VỤ TỔNG HỢP BÀN GIẢN', 351164000, 0, 351164000, 60, 5000000, 90, '272D']]",
           "[['vn2500667324', 'HỢP TÁC XÃ DỊCH VỤ TỔNG HỢP BÀN GIẢN', 351164000, 351164000, '272D']]",
           "['effad1d2-0857-4ac9-8db5-38f2282c0394', 'IB2300047604', 'es-notify-contractor', 'notify-contractor-step-4-kqlcnt', 'CNTTT', 'ba7b1d27-657e-43f1-9589-20b73cb68cf1', 1, 'PTV', '00']",
           '2023-03-31T23:59:59',
           [None],
           []]

def upData_HSMT(details, id1):
    sub_title = "Hồ sơ mời sơ tuyển gói hàng hóa"
    titles1 = 'Số TBMST'

    titles2 = 'Trạng thái thông báo'

    titles3 = 'Bên mời thầu'

    titles4 = 'Loại thông báo'

    titles5 = 'Tên gói thầu'

    titles6 = 'Tên dự án'

    titles7 = 'Chi tiết nguồn vốn'

    titles8 = 'Thời gian phát hành HSMST'

    titles9 = 'Địa điểm nhận HSDST'

    titles10 = 'Thời điểm mở sơ tuyển'

    titles11 = 'Hình thức nhận HSMST'

    titles12 = 'Địa điểm mở HSDST'

    titles13 = 'Hình thức LCNT'

    titles14 = 'Phương thức LCNT'

    titles15 = 'Nội dung chính gói thầu'

    titles16 = 'Thời gian thực hiện hợp đồng'

    titles17 = 'Làm rõ HSMST'

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

    key8 = titles8.strip().lower().replace(' ', '-')
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

    value1 = f"{details[0]}-{details[2]}"

    if details[2] == 0 or details[2] == '00':
        value2 = 'Thông báo đăng lần đầu'
    else:
        value2 = 'Đã điều chỉnh'

    value3 = details[8]

    value4 = "Thông báo thực"

    value5 = details[5]

    value6 = details[27]

    value7 = details[9]

    value8 = None

    value9 = details[18]

    value10 = None

    value11= details[16]

    value12 = details[21]

    value13 = details[11] + str(" có sơ tuyển ") + details[13]

    value14 = details[14]

    value15 = details[6]

    value16 = ""
    for i in details[24]:
        if i.isnumeric(): continue
        else:
            if i == "D":
                value16 = details[15].replace("D", " Ngày")
            elif i == "M":
                value16 = details[15].replace("M", " tháng")

    value17 = None

    records = [
        (key1, sub_title, titles1, value1, id1),
        (key2, sub_title, titles2, value2, id1),
        (key3, sub_title, titles3, value3, id1),
        (key4, sub_title, titles4, value4, id1),
        (key5, sub_title, titles5, value5, id1),
        (key6, sub_title, titles6, value6, id1),
        (key7, sub_title, titles7, value7, id1),
        (key8, sub_title, titles8, value8, id1),
        (key9, sub_title, titles9, value9, id1),
        (key10, sub_title, titles10, value10, id1),
        (key11, sub_title, titles11, value11, id1),
        (key12, sub_title, titles12, value12, id1),
        (key13, sub_title, titles13, value13, id1),
        (key14, sub_title, titles14, value14, id1),
        (key15, sub_title, titles15, value15, id1),
        (key16, sub_title, titles16, value16, id1),
        (key17, sub_title, titles17, value17, id1),
    ]
    conn =connectdb.connect()
    cur = conn.cursor()
    sql = "INSERT INTO pccc_app_bidding_news_details(`key`, sub_title, title, value, news_id, type_id, created_at, updated_at) " \
          f"VALUES (%s, %s, %s, %s, %s, 2, NOW(), NOW());"
    cur.executemany(sql, records)
    conn.commit()

    sql = "SELECT * FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (value10,)
    cur.execute(sql, val)
    a = cur.fetchone()
    conn.commit()
    if a is None:
        myresult = ""
    else:
        myresult = a[0]

    if myresult != "":
        sql = f"UPDATE pccc_app_bidding_news_details SET subject_id = '{myresult}', subject_type = 'App\Models\JobCompanyProfile' WHERE `title` = 'Chủ đầu tư' AND news_id = '{id}';"
        cur.execute(sql)
        conn.commit()
# upData_CNTTT(details, 1841085)
# upData_DXT_TV(details, 1841085)
# upData(details, 1841085)