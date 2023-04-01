import json
import requests
import connectdb

def upData_CNTTT(list, news_id):
    conn = connectdb.connect()
    cursor = conn.cursor()
    for i in list:
        print(f"i------{i}")
        data = ()
        if i['name'] == None:
            goods_name = ''
        else:
            goods_name = i['name']
        label = i['label']
        mass = i['qty']
        unit = i['uom']
        description = ''
        origin = i['origin']
        unit_price = str('{:,}'.format(int(i['amount'])).replace(',', '.')) + ' VND'
        data = (news_id, goods_name, label, mass, unit, description, origin, unit_price, )
        sql = 'INSERT INTO pccc_app_bidding_result_goods(news_id, goods_name, marks_labels_of_products, mass, unit, description, origin, unit_price, created_at, updated_at)' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())'
        cursor.execute(sql, data)
        conn.commit()

# cookies = {
#     'COOKIE_SUPPORT': 'true',
#     'GUEST_LANGUAGE_ID': 'vi_VN',
#     '_ga': 'GA1.1.1974937140.1679213148',
#     'citrix_ns_id': 'AAQ7x-YkZDtAwuoAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==Pe4kZA==aOPkk_D58tljli-zIz8PvdsaJD0=',
#     'JSESSIONID': 'y7dWMWQDTkksvny4pRKJoOR-jH5YPpcmAZxk4TZv.dc_app1_02',
#     'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
#     '_ga_19996Z37EE': 'GS1.1.1680139977.14.1.1680142832.0.0.0',
#     'LFR_SESSION_STATE_20103': '1680142836808',
# }
#
# headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/json',
#     # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; citrix_ns_id=AAQ7x-YkZDtAwuoAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==Pe4kZA==aOPkk_D58tljli-zIz8PvdsaJD0=; JSESSIONID=y7dWMWQDTkksvny4pRKJoOR-jH5YPpcmAZxk4TZv.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1680139977.14.1.1680142832.0.0.0; LFR_SESSION_STATE_20103=1680142836808',
#     'Origin': 'https://muasamcong.mpi.gov.vn',
#     'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=f31ce129-f6fe-4595-94b9-c2a243ac4cf5&notifyId=f31ce129-f6fe-4595-94b9-c2a243ac4cf5&inputResultId=ae2911f4-c140-491a-90a0-63810c62887e&bidOpenId=7047f5e6-48c1-4e83-9a95-a1f3dacccc6d&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300047607&planNo=PL2300031212&pno=undefined',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }
#
# data = '{"id":"ae2911f4-c140-491a-90a0-63810c62887e"}'
# response = requests.post(
#    'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/contractor-input-result/get',
#     cookies=cookies,
#     headers=headers,
#     data=data,
#     allow_redirects=False,
#     verify=False,
# )
#
# data = response.json()
# data_list = data['bideContractorInputResultDTO']['lotResultDTO'][0]['goodsList']
# reviews = json.loads(data_list)
# for review in reviews:
#     print(review['formValue']['lotContent']['Table'])
#
# upData_CNTTT(review['formValue']['lotContent']['Table'], 1841273)
#
