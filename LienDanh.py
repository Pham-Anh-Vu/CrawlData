import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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