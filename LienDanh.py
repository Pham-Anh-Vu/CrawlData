import requests

def liendanh(data):#CNTTT
    listLienDanh = []
    if data is not None:
        if data['bideContractorInputResultDTO']['lotResultDTO'] is not None:
            for i in data['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList']:
                for j in i:
                    if j == 'ventureName':
                        listLienDanh.append(i[j])
    return listLienDanh

def liendanh_DXT(data):
    listLienDanh = []
    listLienDanhChinh = []
    if data is not None:
        if data['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is not None:
            for i in data['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
                if i['ventureName'] is not None:
                    listLienDanh.append(i['ventureName'])
                    listLienDanhChinh.append(i['ventureCode'])
    return listLienDanh, listLienDanhChinh
cookies = {
    'COOKIE_SUPPORT': 'true',
    'GUEST_LANGUAGE_ID': 'vi_VN',
    '_ga': 'GA1.1.1974937140.1679213148',
    'JSESSIONID': 'ju-LA5PqcFZpJvrola-5BpI8rsX2Jps938y1nJUW.dc_app1_02',
    'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
    'LFR_SESSION_STATE_20103': '1680487226161',
    '_ga_19996Z37EE': 'GS1.1.1680485698.23.1.1680487253.0.0.0',
    'citrix_ns_id': 'AAU7Ny0qZDtrcvIAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==2jYqZA==XXnh_W1-Z_a884_6CV6Rs1vSitk=',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.1974937140.1679213148; JSESSIONID=ju-LA5PqcFZpJvrola-5BpI8rsX2Jps938y1nJUW.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1680487226161; _ga_19996Z37EE=GS1.1.1680485698.23.1.1680487253.0.0.0; citrix_ns_id=AAU7Ny0qZDtrcvIAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==2jYqZA==XXnh_W1-Z_a884_6CV6Rs1vSitk=',
    'Origin': 'https://muasamcong.mpi.gov.vn',
    'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=28e4fec2-2d0f-4e9b-bb77-23739c4792b5&notifyId=28e4fec2-2d0f-4e9b-bb77-23739c4792b5&inputResultId=undefined&bidOpenId=618edc2e-4653-4483-9401-82b048eea6a2&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300046552&planNo=PL2300032719&pno=undefined',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
data = '{"notifyNo":"IB2300046552","type":"TBMT","packType":0}'
response = requests.post(
   'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/ldtkqmt/bid-notification-p/get-by-id',
    cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
    timeout=30,
)

data = response.json()
listLienDanh = []
listLienDanhChinh = []
print(data['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'])
for i in data['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
    listLienDanh.append(i['ventureName'])
    listLienDanhChinh.append(i['ventureCode'])

print(listLienDanh)
