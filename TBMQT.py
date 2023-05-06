import requests

import upABNDetail_db
import upABN_db
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def MaTBMQT(page_number):
    for page in range(page_number):
        cookies = {
            'COOKIE_SUPPORT': 'true',
            'GUEST_LANGUAGE_ID': 'vi_VN',
            '_ga': 'GA1.1.1974937140.1679213148',
            'JSESSIONID': 'hwtqrWCt1hAfj1THy7GxX8oQGXiK11vvMmCSME41.dc_app1_01',
            'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
            'LFR_SESSION_STATE_20103': '1683253418696',
            'citrix_ns_id': 'AAY73FpUZDtCyTABAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==N25UZA==kFDFFCJ6l93F5YFOAFzY-JeX17A=',
            '_ga_19996Z37EE': 'GS1.1.1683249887.38.1.1683253940.0.0.0',
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; JSESSIONID=hwtqrWCt1hAfj1THy7GxX8oQGXiK11vvMmCSME41.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1683253418696; citrix_ns_id=AAY73FpUZDtCyTABAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==N25UZA==kFDFFCJ6l93F5YFOAFzY-JeX17A=; _ga_19996Z37EE=GS1.1.1683249887.38.1.1683253940.0.0.0',
            'Origin': 'https://muasamcong.mpi.gov.vn',
            'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index&indexSelect=null',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = '{"pageSize":8,"pageNumber":"' + str(page) + '","query":[{"index":"es-contractor-selection","matchType":"all-1","matchFields":["notifyNo","bidName"],"filters":[{"fieldName":"type","searchType":"in","fieldValues":["es-pre-notify-contractor"]},{"fieldName":"investField","searchType":"in","fieldValues":["TV"]}]}]}'
        response = requests.post(
           'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/smart/search',
           cookies=cookies,
           headers=headers,
           data=data,
            allow_redirects=False,
            verify=False,
        )
        list_id = []
        ids = response.json()['page']['content']
        if ids != None:
            for i in ids:
                CrawlDetail_TBMQT(i['id'])


def CrawlDetail_TBMQT(id):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.1974937140.1679213148',
        'JSESSIONID': 'hwtqrWCt1hAfj1THy7GxX8oQGXiK11vvMmCSME41.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1683253397420',
        '_ga_19996Z37EE': 'GS1.1.1683249887.38.1.1683253402.0.0.0',
        'citrix_ns_id': 'AAY73FpUZDtCyTABAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==H2xUZA==maRAJ-jkTTypNGR5xnIxjsIuhK8=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; JSESSIONID=hwtqrWCt1hAfj1THy7GxX8oQGXiK11vvMmCSME41.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1683253397420; _ga_19996Z37EE=GS1.1.1683249887.38.1.1683253402.0.0.0; citrix_ns_id=AAY73FpUZDtCyTABAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==H2xUZA==maRAJ-jkTTypNGR5xnIxjsIuhK8=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-pre-notify-contractor&stepCode=pre-notify-contractor-step-1-tbmst&id=2f395b1a-6cd6-4fbb-8f16-c129fc76754a&notifyId=2f395b1a-6cd6-4fbb-8f16-c129fc76754a&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=KHAC&bidMode=undefined&notifyNo=IB2200018576&planNo=undefined&pno=undefined&step=tbmqt',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = str(str('{"id":"') + str(id) + str('"}'))
    response = requests.post(
       'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/ebid/pre-notify-contractor-view/detail',
        cookies=cookies,
        headers=headers,
        data=data,
        allow_redirects=False,
        verify=False,
    )

    json_data = response.json()
    review1 = response.json()

    if review1['isInternet'] is None:
        review1['isInternet'] = 0

    if review1['notifyNo'] is None:
        review1['notifyNo'] = 0

    if review1['bidCancelingResponse']['publicDate'] is None:
        review1['bidCancelingResponse']['publicDate'] = 0

    if review1['planNo'] is None:
        review1['planNo'] = 0

    if review1['planType'] is None:
        review1['planType'] = 0
    else:
        if review1['planType'] == 'DTPT':
            review1['planType'] = 'Chi đầu tư phát triển'
        elif review1['planType'] == 'TX':
            review1['planType'] = 'Chi thường xuyên'

    if review1['investField'] is None:
        review1['investField'] = ''
    else:
        if review1['investField'] == 'XL':
            review1['investField'] = 'Xây lắp'
        elif review1['investField'] == 'TV':
            review1['investField'] = 'Tư vấn'
        elif review1['investField'] == 'PTV':
            review1['investField'] = 'Phi tư vấn'
        elif review1['investField'] == 'HH':
            review1['investField'] = 'Hàng hóa'

    if review1['planName'] is None:
        review1['planName'] = 0

    if review1['bidName'] is None:
        review1['bidName'] = 0

    if review1['investorName'] is None:
        review1['investorName'] = 0

    if review1['procuringEntityName'] is None:
        review1['procuringEntityName'] = 0

    if review1['capitalDetail'] is None:
        review1['capitalDetail'] = 0

    if review1['bidForm'] is None:
        review1['bidForm'] = 0
    else:
        if review1['bidForm'] == 'CHCT':
            review1['bidForm'] = 'Chào hàng cạnh tranh'
        if review1['bidForm'] == 'DTRR':
            review1['bidForm'] = 'Đấu thầu rộng rãi'
        if review1['bidForm'] == 'CHCTRG':
            review1['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
        if review1['bidForm'] == 'CDTRG':
            review1['bidForm'] = 'Chỉ định thầu rút gọn'

    if review1['isDomestic'] is None:
        review1['isDomestic'] = 0
    else:
        if review1['isDomestic'] == 1:
            review1['isDomestic'] = 'Trong nước'
        elif review1['isDomestic'] == 0:
            review1['isDomestic'] = 'Quốc tế'

    if review1['bidMode'] is None:
        review1['bidMode'] = 0
    else:
        if review1['bidMode'] == '1_MTHS':
            review1['bidMode'] = 'Một giai đoạn một túi hồ sơ'
        elif review1['bidMode'] == '1_HTHS':
            review1['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

    if review1['isInternet'] is None:
        review1['isInternet'] = 0
    else:
        if review1['isInternet'] == 1:
            review1['isInternet'] = 'Qua mạng'
        elif review1['isInternet'] == 0:
            review1['isInternet'] = 'Không qua mạng'

    if review1['receiveLocation'] is None:
        review1['receiveLocation'] = 0

    if review1['bidCloseDate'] is None:
        review1['bidCloseDate'] = 0

    if review1['bidOpenDate'] is None:
        review1['bidOpenDate'] = 0

    if review1['bidOpenLocation'] is None:
        review1['bidOpenLocation'] = 0

    if review1['bidValidityPeriod'] is None:
        review1['bidValidityPeriod'] = 0

    if review1['bidValidityPeriodUnit'] is None:
        review1['bidValidityPeriodUnit'] = 0

    if review1 is not None:
        if review1['decisionNo'] is None:
            review1['decisionNo'] = 0

        if review1['decisionDate'] is None:
            review1['decisionDate'] = 0

        if review1['decisionAgency'] is None:
            review1['decisionAgency'] = 0

    else:
        review1['decisionNo'] = 0
        review1['decisionDate'] = 0
        review1['decisionAgency'] = 0
        link1 = 0

    if review1['notifyVersion'] is None:
        review1['notifyVersion'] = ''

    if review1['bidPrice'] is None:
        review1['bidPrice'] = 0

    if review1['ctype'] is not None:
        v = review1['ctype']
    else:
        v = 0

    if review1['cperiod'] is None:
        review1['cperiod'] = 0
    if review1['cperiodUnit'] is None:
        review1['cperiodUnit'] = 0
    a = str(review1['cperiod']) + str(review1['cperiodUnit'])

    detail = [
        review1['notifyNo'],  # 0
        review1['bidCancelingResponse']['publicDate'],  # 1
        review1["notifyVersion"],  # 2
        review1['planNo'],  # 3
        review1['planType'],  # 4
        review1['planName'],  # 5
        review1['bidName'],  # 6
        review1['investorName'],  # 7
        review1['procuringEntityName'],  # 8
        review1['capitalDetail'],  # 9
        review1['investField'],  # 10
        review1['bidForm'],  # 11
        v,  # 12
        review1['isDomestic'],  # 13
        review1['bidMode'],  # 14
        a,  # 15
        review1['isInternet'],  # 16
        review1['receiveLocation'],  # 18
        review1['bidCloseDate'],  # 19
        review1['bidOpenDate'],  # 20
        review1['bidOpenLocation'],  # 21
        str(review1['bidValidityPeriod']) + str(review1['bidValidityPeriodUnit']),
        review1['bidPrice'],
        review1["decisionNo"],
        review1['decisionDate'],
        review1['decisionAgency'],
        review1['pname']
    ]
    # print(detail)

# MaTBMQT(4)
    # CrawlDetail_TBMST('a31b7f8f-8b12-4afd-aedc-155d300bf723')
    # time_close = upABN_db.time_close(detail[19])
    # date_ap = upABN_db.time_post(review1['decisionDate'])
    # bid_type = upABN_db.bid_type(review1['investField'])
    # bid_method = upABN_db.bid_method(detail[16])
    # bid_number = detail[0]
    # bid_turn_no = detail[2]
    # type_id = 2
    # if upABN_db.ktTrungDL(review1['notifyNo'], review1["notifyVersion"]) == None:
    #     news_id = upABN_db.upDataDB_HSMT(type_id, bid_type, bid_method, 1, bid_number, bid_turn_no, time_close, date_ap)
    #     upABNDetail_db.upData_HSMT(detail, news_id)
