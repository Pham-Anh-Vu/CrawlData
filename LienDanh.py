import requests

def liendanh():
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.1974937140.1679213148',
        'JSESSIONID': 'nNW_XgqEXGU99SIrxh3SoFGqD0yI4fjiHeBuAzRR.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1680140881109',
        '_ga_19996Z37EE': 'GS1.1.1680139977.14.1.1680140926.0.0.0',
        'citrix_ns_id': 'AAQ7x-YkZDtAwuoAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==BO4kZA==CLNvFvg_y6zzcPbJBs0BoEh5hbI=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; JSESSIONID=nNW_XgqEXGU99SIrxh3SoFGqD0yI4fjiHeBuAzRR.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1680140881109; _ga_19996Z37EE=GS1.1.1680139977.14.1.1680140926.0.0.0; citrix_ns_id=AAQ7x-YkZDtAwuoAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==BO4kZA==CLNvFvg_y6zzcPbJBs0BoEh5hbI=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=4074d297-05bd-4c80-85e5-1ba7ddedd57e&notifyId=4074d297-05bd-4c80-85e5-1ba7ddedd57e&inputResultId=0458021f-06e2-45a8-8c01-b20b4e6d3738&bidOpenId=801d2482-1c43-49d0-8d61-f375ce958916&techReqId=2f70aa7e-4af1-4510-a673-ecb176e68275&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_HTHS&notifyNo=IB2300035936&planNo=PL2300027765&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = '{"id":"0458021f-06e2-45a8-8c01-b20b4e6d3738"}'
    response = requests.post(
       'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/contractor-input-result/get',
        cookies=cookies,
        headers=headers,
        data=data,
        allow_redirects=False,
        verify=False,
    )
    # ['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList']
    data = response.json()
    listLienDanh = []
    for i in data['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList']:
        for j in i:
            if j == 'ventureName':
                listLienDanh.append(i[j])
    return listLienDanh
