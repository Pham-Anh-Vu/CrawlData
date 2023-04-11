import requests

import upABNDetail_db
import upABN_db


def MaHSMT(page_number):
    for page in range(page_number):
        cookies = {
            'COOKIE_SUPPORT': 'true',
            'GUEST_LANGUAGE_ID': 'vi_VN',
            '_ga': 'GA1.1.1974937140.1679213148',
            'JSESSIONID': 'folLSpXdtv174XNqA39fJTtGpmiJbIe-FXwTEAJ8.dc_app1_01',
            'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
            'LFR_SESSION_STATE_20103': '1680937471506',
            '_ga_19996Z37EE': 'GS1.1.1680937317.30.1.1680937479.0.0.0',
            'citrix_ns_id': 'AAM7SRExZDv_B_0AAAAAADuFeyfrzB16Q6f2O3wkwp-X_KBiAk_jQriThj-xlt31Ow==ixUxZA==yENbZewv_YZoxZnrf-LBykb7U7Q=',
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; JSESSIONID=folLSpXdtv174XNqA39fJTtGpmiJbIe-FXwTEAJ8.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1680937471506; _ga_19996Z37EE=GS1.1.1680937317.30.1.1680937479.0.0.0; citrix_ns_id=AAM7SRExZDv_B_0AAAAAADuFeyfrzB16Q6f2O3wkwp-X_KBiAk_jQriThj-xlt31Ow==ixUxZA==yENbZewv_YZoxZnrf-LBykb7U7Q=',
            'Origin': 'https://muasamcong.mpi.gov.vn',
            'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index&indexSelect=null',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = '{"pageSize":8,"pageNumber":"' + str(page) + '","query":[{"index":"es-contractor-selection","matchType":"all","matchFields":["notifyNo","bidName"],"filters":[{"fieldName":"type","searchType":"in","fieldValues":["es-pre-notify-contractor"]},{"fieldName":"investField","searchType":"not_in","fieldValues":["TV"]},{"fieldName":"isInternet","searchType":"in","fieldValues":[1]}]}]}'

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
                CrawlDetail_TBMST(i['id'])

def CrawlDetail_TBMST(id):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.1974937140.1679213148',
        'JSESSIONID': '0iPC8rXywShC2fplUIKfoRlyDjKJcJ0NMCTB8xC4.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1680928833386',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1680927313.28.1.1680928998.0.0.0',
        'citrix_ns_id': 'AAU7JfAwZDuiQP4AAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==avQwZA==ehxEW5of2ciynFoDjc8h7_Udj30=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; JSESSIONID=0iPC8rXywShC2fplUIKfoRlyDjKJcJ0NMCTB8xC4.dc_app1_02; LFR_SESSION_STATE_20103=1680928833386; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1680927313.28.1.1680928998.0.0.0; citrix_ns_id=AAU7JfAwZDuiQP4AAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==avQwZA==ehxEW5of2ciynFoDjc8h7_Udj30=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-pre-notify-contractor&stepCode=pre-notify-contractor-step-3-kqst&id=a31b7f8f-8b12-4afd-aedc-155d300bf723&notifyId=a31b7f8f-8b12-4afd-aedc-155d300bf723&inputResultId=undefined&bidOpenId=4cca958b-3729-4f55-a4b3-687df7d422fa&techReqId=undefined&bidPreNotifyResultId=a4ea7f89-bac3-4655-a277-08d613644bdf&bidPreOpenId=undefined&processApply=LDT&bidMode=1_HTHS&notifyNo=IB2200002959&planNo=undefined&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
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
        fee = ''
    else:
        if review1['isInternet'] == 1:
            if review1['bidForm'] == 'DTRR' or review1['bidForm'] == 'DTHC' or review1['bidForm'] == 'MSTT':
                fee = '330,000 VND'
            elif review1['bidForm'] == 'CHCT' or review1['bidForm'] == 'CHCTRG':
                fee = '220,000 VND'
        elif review1['isInternet'] == 0:
            if review1['feeValue'] is None:
                fee = 'Miễn phí'
            else:
                fee = review1['feeValue']
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
        review1['notifyNo'],#0
        review1['bidCancelingResponse']['publicDate'],#1
        review1["notifyVersion"],  # 2
        review1['planNo'],#3
        review1['planType'],#4
        review1['planName'],#5
        review1['bidName'],#6
        review1['investorName'],#7
        review1['procuringEntityName'],#8
        review1['capitalDetail'],#9
        review1['investField'],#10
        review1['bidForm'],#11
        v,#12
        review1['isDomestic'],#13
        review1['bidMode'],#14
        a,#15
        review1['isInternet'],#16
        fee,#17
        review1['receiveLocation'],#18
        review1['bidCloseDate'],#19
        review1['bidOpenDate'],#20
        review1['bidOpenLocation'],#21
        str(review1['bidValidityPeriod']) + str(review1['bidValidityPeriodUnit']),
        review1['bidPrice'],
        review1["decisionNo"],
        review1['decisionDate'],
        review1['decisionAgency'],
        review1['pname']
    ]

# CrawlDetail_TBMST('a31b7f8f-8b12-4afd-aedc-155d300bf723')
    time_close = upABN_db.time_close(detail[19])
    date_ap = upABN_db.time_post(review1['decisionDate'])
    bid_type = upABN_db.bid_type(review1['investField'])
    bid_method = upABN_db.bid_method(detail[16])
    bid_number = detail[0]
    bid_turn_no = detail[2]
    type_id = 2
    if upABN_db.ktTrungDL(review1['notifyNo'], review1["notifyVersion"]) == None:
        news_id = upABN_db.upDataDB_HSMT(type_id, bid_type, bid_method, 1, bid_number, bid_turn_no, time_close, date_ap)
        upABNDetail_db.upData_HSMT(detail, news_id)
        print(1)