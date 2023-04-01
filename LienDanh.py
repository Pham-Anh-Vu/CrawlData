import requests

def liendanh(data):
    listLienDanh = []
    for i in data['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList']:
        for j in i:
            if j == 'ventureName':
                listLienDanh.append(i[j])
    return listLienDanh
