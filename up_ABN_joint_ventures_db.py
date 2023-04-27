import connectdb

def upData_CNTTT(listLienDanh, news_id, type_id):
    if listLienDanh == None or listLienDanh == [] or listLienDanh == [None]:
        return
    list_id = []
    list_taxCode = []
    list_company = []
    # for i in range(len(listLienDanh)-1):
    #     jv_name = jv_name + listLienDanh[i] + ' - '
    # jv_name = jv_name + listLienDanh[len(listLienDanh)-1]
    jv_name = listLienDanh[0]
    listLienDanh.find()
    listLienDanh = listLienDanh[0].split(' - ')
    kt = 0
    for i in listLienDanh:
        if kt == 0:
            a = i[10:]
            list_company.append(a)
            kt = 1
            continue
        list_company.append(i.rstrip())
    listLienDanh = list_company

    conn = connectdb.connect()
    for i in listLienDanh:
        sql = f"SELECT * FROM pccc_app_job_company_profiles WHERE company_name = '{i}'"
        curses = conn.cursor()
        curses.execute(sql)
        tuple_company = curses.fetchone()
        list_id.append(str(tuple_company[0]))
        list_taxCode.append(tuple_company[15])
    str2 = '('
    for i in range(len(listLienDanh)-1):
        str2 = str2 + list_taxCode[i] + ' - ' + listLienDanh[i] +', '
    str2 = str2 + list_taxCode[len(listLienDanh)-1] + ' - ' + listLienDanh[len(listLienDanh)-1] + ')'

    jv_name = jv_name+str2
    for i in list_id:
        cp_id = i
        for j in list_id:
            if i == j:
                continue
            ven_id = j
            sql = "INSERT INTO pccc_app_bidding_news_joint_ventures(news_id, type_id, joint_venture_name, job_company_profile_id, joint_venture_id, created_at, updated_at)" \
                  "VALUES(%s, %s, %s, %s, %s, NOW(), NOW()) "
            data = (news_id, type_id, jv_name, cp_id, ven_id,)
            curses.execute(sql, data)
            conn.commit()


# list1 = ['CÔNG TY TNHH TƯ VẤN VÀ XÂY DỰNG ADC HÀ NỘI',
#          'CÔNG TY CỔ PHẦN TỰ ĐỘNG HÓA ACS VIỆT NAM',
#          'VIện Dân tộc học']
#
# name = upData_CNTTT(list1, 1838385, 1)
# print(name)
# list_company = []
# kt = 0
# listLienDanh = ['Liên danh Nhà xuất bản Hà Nội - In Phú Thịnh ', 'Liên danh Nhà xuất bản Hà Nội - In Phú Thịnh ']
# listLienDanh = listLienDanh[0].split(' - ')
# for i in listLienDanh:
#     if kt == 0:
#         a = i[10:]
#         list_company.append(a)
#         kt = 1
#         continue
#     list_company.append(i.rstrip())
# listLienDanh = list_company
# print(listLienDanh)