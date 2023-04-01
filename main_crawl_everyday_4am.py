import requests
import datetime
import csv
import urllib3
import threading
import random
import time
import os
import json
import connectdb
from unidecode import unidecode
from datetime import datetime, timedelta

import upABNDetail_db
import upABNFiles_db
import upABN_db
import LienDanh
from pympler import muppy
import upFileDinhKemHSMT
import upABO_db
import upABO_result_complete_gd_hsdt
import upABRGoods_db
import up_ABN_joint_ventures_db
from upABNFiles_db import fileDangTai as fileDangTaidb

global fileDangTai
fileDangTai = fileDangTaidb

global checkListFileDangTai

global list_upFile
list_upFile = []


all_objects = muppy.get_objects()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

yesterday = datetime.now() - timedelta(days=2)

yesterday_str = yesterday.strftime('%Y-%m-%d')

startDay = str(yesterday_str)
endDay = str(yesterday_str)

areaType1 = []

with open('./areaType1.csv', newline='\n', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row == []:
            continue
        areaType1.append(row)

areaType2 = []

with open('./areaType2.csv', newline='\n', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row == []:
            continue
        areaType2.append(row)

areaType3 = []

with open('./areaType3.csv', newline='\n', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row == []:
            continue
        areaType3.append(row)


class MyThread(threading.Thread):
    def __init__(self, threadID, name, step, typeOfThread, pageNumberStart, NumberThreadOfThis):
        threading.Thread.__init__(self=self)

        self.threadID = threadID

        self.name = name

        self.step = step

        self.typeOfThread = typeOfThread

        # time sleep of each thread
        self.i = 0

        self.details = [0]

        self.codes = [0]

        self.session = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20,max_retries=3)
        self.session.mount('http://', self.adapter)
        self.session.mount('https://', self.adapter)

        self.totalPageNumber = 0

        self.pageNumberStart = pageNumberStart

        self.NumberThreadOfThis = NumberThreadOfThis

    def run(self):

        print("Starting " + self.name)

        self.codes.clear()
        self.details.clear()

        if (self.typeOfThread == 'NT'):
            self.totalPageNumber = SoTrangNT


        elif self.typeOfThread == 'BMT':
            self.totalPageNumber = SoTrangBMT


        elif self.typeOfThread == 'TT':
            self.totalPageNumber = SoTrangTT


        elif self.typeOfThread == 'DT':
            self.totalPageNumber = SoTrangDT

        if self.totalPageNumber >= 1:

            self.folder_path1 = folder_path

            self.pageNumberEnd = self.totalPageNumber - 1

            self.pageNumber = self.pageNumberStart

            for z in range(((self.pageNumberEnd - self.pageNumberStart) // self.NumberThreadOfThis) + 1):

                if self.pageNumber > self.pageNumberEnd:
                    break

                if self.typeOfThread == 'NT':

                    CrawlMaNhaThau(pageNumber=self.pageNumber, codes=self.codes, details=self.details,
                                   session1=self.session, folder_path1=self.folder_path1)

                elif self.typeOfThread == 'BMT':

                    CrawlMaBenMoiThau(pageNumber=self.pageNumber, codes=self.codes, details=self.details,
                                      session1=self.session, folder_path1=self.folder_path1)

                elif self.typeOfThread == 'TT':

                    CrawlMaTinTuc(pageNumber=self.pageNumber, codes=self.codes, details=self.details,
                                  session1=self.session, folder_path1=self.folder_path1)

                elif self.typeOfThread == 'DT':

                    CrawlMaTinTucDongThau(pageNumber=self.pageNumber, codes=self.codes, details=self.details,
                                          session1=self.session, folder_path1=self.folder_path1)
                
                elif self.typeOfThread == 'upData':
                    main()

                if random.randrange(1, 4) == 2:
                    self.session.close()
                    self.session = requests.Session()

                self.pageNumber = self.pageNumber + self.step

class MyThread2(threading.Thread):
    def __init__(self, threadID, name, step, typeOfThread, list_upFile1):
        threading.Thread.__init__(self=self)

        self.threadID = threadID

        self.name = name

        self.step = step

        self.typeOfThread = typeOfThread

        # time sleep of each thread
        self.i = 0

        self.details = [0]

        self.codes = [0]

        self.session = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20,max_retries=3)
        self.session.mount('http://', self.adapter)
        self.session.mount('https://', self.adapter)

        if len(list_upFile) >= int(self.threadID):
            if list_upFile != []:
                self.list = list_upFile1[int(self.threadID)]
                self.list_upFile2 = self.list[0]
                self.code_file = self.list[1]
            else:
                self.list = []
                self.list_upFile2 = ''
                self.code_file = 0
        else:
            self.list = []
            self.list_upFile2 = ''
            self.code_file = 0
        
    def run(self):
        print("Starting upFile" + self.name)
        while True:
            if self.list != []:
                del list_upFile[self.threadID]
                self.media_id, self.file_name_for_user, self.url = up_pccc_app_medias(self.list_upFile2)
                update_pccc_news_files(self.media_id, self.file_name_for_user, self.url, self.code_file)
                if len(list_upFile) >= int(self.threadID) :
                    self.list = self.list_upFile1[int(self.threadID)]
                    self.list_upFile2 = self.list[0]
                    self.code_file = self.list[1]
                else:
                    self.list = []
                    self.list_upFile2 = ''
                    self.code_file = 0

def update_pccc_news_files(media_id, file_name_for_user, url, code_file):
    conn = connectdb.connect()
    cur = conn.cursor()
    sql = 'SELECT id FROM pccc_app_bidding_news_files WHERE file_name = %s ORDER BY created_at DESC'
    val = ('File đang tải' +str(code_file),)
    cur.execute(sql, val)
    myresult = cur.fetchone()
    if myresult != []:
        news_files_id = myresult[0]
    
    sql = 'UPDATE pccc_app_bidding_news_files SET file_name = %s , link_muasamcong = %s , media_id=%s , updated_at = NOW() WHERE `id` = %s'
    val = (file_name_for_user, url, media_id,news_files_id)
    cur.execute(sql, val)
    conn.commit()
    
def upData(details, result, link1, fileDangTai):
    id1 = details[33][0]
    object_type = 'App\Models\BiddingNewsDetail'
    object_id = int(result)
    record = []
    media_id = None
    record.append([object_type, object_id, 'Quyết định phê duyệt', link1 ,media_id, 1])
    fileDangTai1 = fileDangTai
    for i in details[35]:
        bidform = i[4]
        link = f"https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode={bidform}&id={id1}"
        filename = i[3]
        if filename == "Quyết định phê duyệt":
            tuples = (object_type, object_id, filename, link, media_id, 1)
            record.append(tuples)
        else:
            tuples = (object_type, object_id, filename, link, media_id, None)
            record.append(tuples)
        for z in details[37]:
            if i[5] == z[2]:
                if z[1] == i[4]:
                    list_upFile.append([z[0],fileDangTai1])
                    tuples = (object_type, object_id, 'File đang tải '+str(fileDangTai1), None, None, None)
                    fileDangTai1 = fileDangTai1 +1
                    record.append(tuples)

                else:
                    if z[2] == 'P2':
                        list_upFile.append([z[0],fileDangTai1])
                        tuples = (object_type, object_id, 'File đang tải '+str(fileDangTai1), None, None, None)
                        fileDangTai1 = fileDangTai1 +1
                        record.append(tuples)
            else:
                if z[2]=='C8':
                    if i[4] == 'C8':
                        list_upFile.append([z[0],fileDangTai1])
                        tuples = (object_type, object_id, 'File đang tải '+str(fileDangTai1), None, None, None)
                        fileDangTai1 = fileDangTai1 +1
                        record.append(tuples)
            
    conn = connectdb.connect()
    cur = conn.cursor()
    for recordx in record:
        sql = "INSERT INTO pccc_app_bidding_news_files (object_type, object_id, file_name, link_muasamcong, media_id, created_at, updated_at, is_big_file) VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s);"
        cur.execute(sql, recordx)
        conn.commit()

    return fileDangTai1


def up_pccc_app_medias(code):
    url = 'http://localhost:1234/api/download/file/browser/public?fileId='+code
    """name = 'a.pdf'
    type = 'pdf'
    path = 'a'
    file_name_for_user = 'a.pdf'"""
    name,type,path, file_name_for_user = upFileDinhKemHSMT.downFileAndUpLoad(url=url)
    conn = connectdb.connect()
    cur = conn.cursor()
    sql= "INSERT INTO pccc_app_medias (name, type, path, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())"
    val = (name, type, path)
    cur.execute(sql,val)
    conn.commit()
    media_id = cur.lastrowid
    media_id = int(media_id)
    return media_id, file_name_for_user, url

def main():
    numberOfThread = 5
    threadUpFile = 5
    threads = []
    for i in range(numberOfThread):
        a = i + 1
        b = str(a)
        thread = MyThread2(i, "thread" + b, threadUpFile, 'upFile', list_upFile)
        threads.append(thread)
        thread.start()

def SoTrangNhaThau(startDay, endDay):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'hpt9WsBRmb5FEwVIvYY_bxdgHRX4efWskGxOPs55.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1676953840653',
        '_ga_19996Z37EE': 'GS1.1.1676953826.16.1.1676954039.0.0.0',
        'citrix_ns_id': 'AAY74Ej0YzsGLrEAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==Tk30Yw==IE3IODMJYe6g6wMNdkWr6gpUBoQ=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=hpt9WsBRmb5FEwVIvYY_bxdgHRX4efWskGxOPs55.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1676953840653; _ga_19996Z37EE=GS1.1.1676953826.16.1.1676954039.0.0.0; citrix_ns_id=AAY74Ej0YzsGLrEAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==Tk30Yw==IE3IODMJYe6g6wMNdkWr6gpUBoQ=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/approved-contractors-list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    totalPageNumber = 0

    try:
        data = '{"pageSize":10,"pageNumber":0,"queryParams":{"officePro":{"contains":null},"effRoleDate":{"greaterThanOrEqual":"' + str(
            startDay) + 'T00:00:00.000Z","lessThanOrEqual":"' + str(
            endDay) + 'T23:59:59.000Z"},"isForeignInvestor":{"equals":null},"roleType":{"equals":"NT"},"decNo":{"contains":null},"orgName":{"contains":null},"taxCode":{"contains":null},"orgNameOrOrgCode":{"contains":null},"agencyName":{"in":null}}}'
        response = requests.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractors-approved/services/get-list',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
        )
        json_data = response.json()
        totalPageNumber = json_data['totalPages']


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang nha thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang nha thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang nha thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang nha thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        pass

    return totalPageNumber


def CrawlMaNhaThau(pageNumber, codes, details, session1, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'hpt9WsBRmb5FEwVIvYY_bxdgHRX4efWskGxOPs55.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1676953840653',
        '_ga_19996Z37EE': 'GS1.1.1676953826.16.1.1676954039.0.0.0',
        'citrix_ns_id': 'AAY74Ej0YzsGLrEAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==Tk30Yw==IE3IODMJYe6g6wMNdkWr6gpUBoQ=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=hpt9WsBRmb5FEwVIvYY_bxdgHRX4efWskGxOPs55.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1676953840653; _ga_19996Z37EE=GS1.1.1676953826.16.1.1676954039.0.0.0; citrix_ns_id=AAY74Ej0YzsGLrEAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==Tk30Yw==IE3IODMJYe6g6wMNdkWr6gpUBoQ=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/approved-contractors-list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"pageSize":10,"pageNumber":' + str(
            pageNumber) + ',"queryParams":{"officePro":{"contains":null},"effRoleDate":{"greaterThanOrEqual":"' + str(
            startDay) + 'T00:00:00.000Z","lessThanOrEqual":"' + str(
            endDay) + 'T23:59:59.000Z"},"isForeignInvestor":{"equals":null},"roleType":{"equals":"NT"},"decNo":{"contains":null},"orgName":{"contains":null},"taxCode":{"contains":null},"orgNameOrOrgCode":{"contains":null},"agencyName":{"in":null}}}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractors-approved/services/get-list',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data = response.json()
        reviews = json_data['content']
        for review in reviews:
            if review['orgCode'] is None:
                review['orgCode'] = 0

            if review['officeAdd'] is None:
                review['officeAdd'] = 0

            if review['status'] is None:
                review['status'] = 4
            else:
                if review['status'] == 1:
                    review['status'] = 'Đang hoạt động'
                elif review['status'] == 2:
                    review['status'] = 'Tạm ngừng'
                elif review['status'] == 0:
                    review['status'] = 'Chấm dứt'

            if review['startPendingDate'] is None:
                review['startPendingDate'] = 0

            codes.append([review['orgCode'], review['officeAdd'], review['status'], review['startPendingDate']])

        for code in codes:
            CrawlDetailNhaThau(code=code[0], details=details, session1=session, codes=code, folder_path1=folder_path1)

        codes.clear()
        details.clear()
        i = random.randrange(1, 10)
        time.sleep(i)

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu nha thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu nha thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Ho so bi loi khong lay duoc du lieu nha thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu nha thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    return


def CrawlDetailNhaThau(code, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'UnaoWtATytMT5PiDD6kaqPbzQYtjOI4SwRUYaH-5.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1676970311696',
        '_ga_19996Z37EE': 'GS1.1.1676970250.19.1.1676970321.0.0.0',
        'citrix_ns_id': 'AAE7CIn0Yzt-YLAAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==2Yz0Yw==QMHJAJKtD9JRuqiJJFd4xKmRYg0=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=UnaoWtATytMT5PiDD6kaqPbzQYtjOI4SwRUYaH-5.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1676970311696; _ga_19996Z37EE=GS1.1.1676970250.19.1.1676970321.0.0.0; citrix_ns_id=AAE7CIn0Yzt-YLAAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==2Yz0Yw==QMHJAJKtD9JRuqiJJFd4xKmRYg0=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/approved-contractors-list?p_p_id=egpportalcontractorsapproved_WAR_egpportalcontractorsapproved&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorsapproved_WAR_egpportalcontractorsapproved_render=detail&orgCode=vn2700949654&effRoleDate=17/2/2023',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"orgCode":"' + str(code) + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractors-approved/services/get-detail-approve-bidder',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify= False,
            timeout=30,
        )
        json_data = response.json()
        reviews = json_data

        if reviews['orgFullName'] is None:
            reviews['orgFullName'] = ''

        if reviews['orgEnName'] is None:
            reviews['orgEnName'] = ''

        if reviews['orgCode'] is None:
            reviews['orgCode'] = ''

        if reviews['businessType'] is None:
            reviews['businessType'] = ''

        if reviews['taxCode'] is None:
            reviews['taxCode'] = ''

        if reviews['taxDate'] is None:
            reviews['taxDate'] = ''

        if reviews['taxNation'] is None:
            reviews['taxNation'] = ''

        if reviews['officeWar'] is None:
            reviews['officeWar'] = ''

        if reviews['officeWeb'] is None:
            reviews['officeWeb'] = ''

        if reviews['repName'] is None:
            reviews['repName'] = ''

        if reviews['repPosition'] is None:
            reviews['repPosition'] = ''

        nhap = [0]
        nhap.clear()
        if reviews['businesses'] is None:
            reviews['businesses'] = ''
        else:
            for review in reviews['businesses']:
                nhap.append([review['code'], review['name'], review['main']])

        details.extend([reviews["orgFullName"],
                        reviews['orgEnName'],
                        reviews['orgCode'],
                        reviews['businessType'],
                        reviews['taxCode'],
                        reviews['taxDate'],
                        reviews['taxNation'],
                        codes[1],
                        reviews['officeWar'],
                        reviews['officeWeb'],
                        reviews['repName'],
                        reviews['repPosition'],
                        codes[2],
                        codes[3],
                        nhap])

        if details[8] != '':
            ma = details[8]
            matinh = ma[:3]
            maquan = ma[:5]
            maphuong = ma

            for codeT in areaType1:
                if matinh == codeT[0]:
                    matinh = codeT[2]

            for codeQ in areaType2:
                if maquan == codeQ[0]:
                    maquan = codeQ[2]
            for codeH in areaType3:
                if maphuong == codeH[0]:
                    maphuong = codeH[2]

            if details[7] != '':
                company_address = details[7] + ', ' + maphuong + ', ' + maquan + ', ' + matinh
            else:
                company_address = maphuong + ', ' + maquan + ', ' + matinh

        else:
            if details[7] != '':
                company_address = details[7]
            else:
                company_address = None

        if details[0] != '':
            company_name = details[0]
        else:
            company_name = None

        if details[9] != '':
            company_website = details[9]
        else:
            company_website = None

        if details[4] != '':
            tax_code = details[4]
        else:
            tax_code = details[4]

        if details[5] != '':
            operation_date = details[5]
            date_string = operation_date
            operation_date = datetime.fromisoformat(date_string.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        else:
            operation_date = None

        contractor = 1

        conn = connectdb.connect()
        cur = conn.cursor()
        sql = "SELECT id FROM pccc_app_job_company_profiles WHERE `company_name` = %s"
        val = (company_name,)
        cur.execute(sql, val)

        myresult = cur.fetchall()
        status = 'Đã duyệt'

        if myresult == []:
            sql = "INSERT INTO pccc_app_job_company_profiles (company_name, company_address, company_website, tax_code, operation_date, contractor, created_at, updated_at, status) VALUES (%s, %s, %s, %s, %s, %s, NOW(),NOW(),%s)"
            val = (company_name, company_address, company_website, tax_code, operation_date, contractor, status)
            cur.execute(sql, val)
            conn.commit()
            job_company_profile_id = cur.lastrowid

        else:
            sql = "UPDATE pccc_app_job_company_profiles SET contractor = 1, updated_at = NOW() WHERE company_name = %s"
            val = (company_name,)
            cur.execute(sql, val)
            conn.commit()
            job_company_profile_id = myresult[-1][0]

        s = details[14]
        s1 = s

        for nganh in s1:
            career_name = nganh[1]
            sql = "SELECT * FROM pccc_app_company_career WHERE job_company_profile_id = %s AND career_name = %s"
            val = (job_company_profile_id, career_name)
            cur.execute(sql, val)
            myresult = cur.fetchall()
            if myresult == []:
                sql = "INSERT INTO pccc_app_company_career (job_company_profile_id,career_name,created_at,updated_at) VALUES (%s, %s,NOW(),NOW())"
                val = (job_company_profile_id, career_name)
                cur.execute(sql, val)
                conn.commit()

        with open('' + folder_path1 + '/nhathau.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so nha thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so nha thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so nha thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so nha thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    return


def SoTrangBenMoiThau(startDay, endDay):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'rQFZTNUBUxbaI3eiLusPCF03kaD8ShshYAVCrV4X.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1676974814.20.1.1676977060.0.0.0',
        'LFR_SESSION_STATE_20103': '1676977061801',
        'citrix_ns_id': 'AAQ7cZf0YztV3rEAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==Oaf0Yw==hWaYUuAt23QlIdj3PMMkri__EDQ=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=rQFZTNUBUxbaI3eiLusPCF03kaD8ShshYAVCrV4X.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1676974814.20.1.1676977060.0.0.0; LFR_SESSION_STATE_20103=1676977061801; citrix_ns_id=AAQ7cZf0YztV3rEAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==Oaf0Yw==hWaYUuAt23QlIdj3PMMkri__EDQ=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/bid-solicitor-approval',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    totalPageNumber = 0

    try:
        data = '{"pageSize":10,"pageNumber":0,"queryParams":{"roleType":{"equals":"BMT"},"orgName":{"contains":null},"orgCode":{"contains":""},"orgNameOrOrgCode":{"contains":null},"agencyName":{"in":null},"effRoleDate":{"greaterThanOrEqual":"' + startDay + 'T00:00:00.000Z","lessThanOrEqual":"' + endDay + 'T23:59:59.000Z"}}}'
        response = requests.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-bid-solicitor-approved/services/um/lookup-orgInfo',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
        )
        json_data = response.json()
        reviews = json_data
        totalPageNumber = reviews['ebidOrgInfos']['totalPages']

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang ben moi thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang ben moi thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang ben moi thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang ben moi thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    return totalPageNumber


def CrawlMaBenMoiThau(pageNumber, codes, details, session1, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'rQFZTNUBUxbaI3eiLusPCF03kaD8ShshYAVCrV4X.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1676977061801',
        '_ga_19996Z37EE': 'GS1.1.1676974814.20.1.1676977153.0.0.0',
        'citrix_ns_id': 'AAQ7cZf0YztV3rEAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==iKf0Yw==EkDLV_tWQFTT1oeLU7-DxK1ab8w=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=rQFZTNUBUxbaI3eiLusPCF03kaD8ShshYAVCrV4X.dc_app1_02; LFR_SESSION_STATE_20103=1676977061801; _ga_19996Z37EE=GS1.1.1676974814.20.1.1676977153.0.0.0; citrix_ns_id=AAQ7cZf0YztV3rEAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==iKf0Yw==EkDLV_tWQFTT1oeLU7-DxK1ab8w=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/bid-solicitor-approval',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"pageSize":10,"pageNumber":' + str(
            pageNumber) + ',"queryParams":{"roleType":{"equals":"BMT"},"orgName":{"contains":null},"orgCode":{"contains":""},"orgNameOrOrgCode":{"contains":null},"agencyName":{"in":null},"effRoleDate":{"greaterThanOrEqual":"' + startDay + 'T00:00:00.000Z","lessThanOrEqual":"' + endDay + 'T23:59:59.000Z"}}}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-bid-solicitor-approved/services/um/lookup-orgInfo',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data = response.json()
        reviews = json_data["ebidOrgInfos"]["content"]

        for review in reviews:

            if (review['effRoleDate']) is None:
                a = 0

            else:
                a = str(review['effRoleDate'][2]) + '/' + str(review['effRoleDate'][1]) + '/' + str(
                    review['effRoleDate'][0])

            if review['orgCode'] is None:
                review['orgCode'] = 0

            codes.append([review['orgCode'], a])

        for code in codes:
            CrawlDetailBenMoiThau(code=code[0], details=details, session1=session, codes=code,
                                  folder_path1=folder_path1)


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu ben moi thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu ben moi thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu ben moi thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu ben moi thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    return


def CrawlDetailBenMoiThau(code, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'LGPSAiiI5Py7FqUFtVrdIdpwpw1KE-NmKmk2rzNf.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1676974814.20.1.1676979144.0.0.0',
        'LFR_SESSION_STATE_20103': '1676979159262',
        'citrix_ns_id': 'AAQ7E6v0YzsK7rEAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==aa_0Yw==FM3fa9e5hr-wmhFJZWmrf8o0yNo=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=LGPSAiiI5Py7FqUFtVrdIdpwpw1KE-NmKmk2rzNf.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1676974814.20.1.1676979144.0.0.0; LFR_SESSION_STATE_20103=1676979159262; citrix_ns_id=AAQ7E6v0YzsK7rEAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==aa_0Yw==FM3fa9e5hr-wmhFJZWmrf8o0yNo=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/bid-solicitor-approval?p_p_id=egpportalbidsolicitorapproved_WAR_egpportalbidsolicitorapproved&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalbidsolicitorapproved_WAR_egpportalbidsolicitorapproved_render=detail&tendererCode=vnz000027621&startPendingDate=null&status=1&effectRoleDate=20/2/2023',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"orgCode":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-bid-solicitor-approved/services/um/org/get-detail-info',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data = response.json()
        if json_data is not None:
            reviews = json_data['orgInfo']
        else:
            return

        if reviews['orgFullName'] is None:
            reviews['orgFullName'] = ''

        if reviews['orgEnName'] is None:
            reviews['orgEnName'] = ''

        if reviews['orgCode'] is None:
            reviews['orgCode'] = ''

        if reviews['businessType'] is None:
            reviews['businessType'] = ''
        else:
            if reviews['businessType'] == 'LLC2':
                reviews['businessType'] = 'Công ty trách nhiệm hữu hạn hai thành viên trở lên'
            elif reviews['businessType'] == 'LLC1':
                reviews['businessType'] = 'Công ty trách nhiệm hữu hạn một thành viên'
            elif reviews['businessType'] == 'NON_BUSINESS_UNIT':
                reviews['businessType'] = 'Đơn vị hành chính, đơn vị sự nghiệp'
            elif reviews['businessType'] == 'LEGAL_TYPE_COOP':
                reviews['businessType'] = 'Hợp tác xã'
            elif reviews['businessType'] == 'ECONOMY_ORG':
                reviews['businessType'] = 'Tổ chức kinh tế của tổ chức chính trị, xã hội'
            elif reviews['businessType'] == 'LEGAL_TYPE_OTHER':
                reviews['businessType'] = 'Loại hình khác'
            elif reviews['businessType'] == 'BR':
                reviews['businessType'] = 'Chi nhánh'
            elif reviews['businessType'] == 'PS':
                reviews['businessType'] = 'Công ty hợp danh'
            elif reviews['businessType'] == 'PE':
                reviews['businessType'] = 'Doanh nghiệp tư nhân'
            elif reviews['businessType'] == 'RO':
                reviews['businessType'] = 'Văn phòng đại diện'
            elif reviews['businessType'] == 'BL':
                reviews['businessType'] = 'Địa điểm kinh doanh'
            elif reviews['businessType'] == 'SC':
                reviews['businessType'] = 'Công ty cổ phần'

        if reviews['taxDate'] is None:
            reviews['taxDate'] = ''
        else:
            timestamp = reviews['taxDate'] // 1000
            dt = datetime.fromtimestamp(timestamp)
            reviews['taxDate'] = dt.strftime("%Y-%m-%d %H:%M:%S")

        if reviews['taxCode'] is None:
            reviews['taxCode'] = ''

        if reviews['taxNation'] is None:
            reviews['taxNation'] = ''

        if reviews['statusOrg'] is None:
            reviews['statusOrg'] = ''
        else:
            if reviews['statusOrg'] == 1:
                reviews['statusOrg'] = 'Đang hoạt động'
            elif reviews['statusOrg'] == 2:
                reviews['statusOrg'] = 'Tạm ngừng'
            elif reviews['statusOrg'] == 3:
                reviews['statusOrg'] = 'Chấm dứt'

        if reviews['agencyName'] is None:
            reviews['agencyName'] = ''

        if reviews['budgetCode'] is None:
            reviews['budgetCode'] = ''

        if reviews['officeAdd'] is None:
            reviews['officeAdd'] = ''

        if reviews['officePhone'] is None:
            reviews['officePhone'] = ''

        if reviews['officeWeb'] is None:
            reviews['officeWeb'] = ''

        if reviews['repName'] is None:
            reviews['repName'] = ''

        if reviews['repPosition'] is None:
            reviews['repPosition'] = ''

        if reviews['repPhone'] is None:
            reviews['repPhone'] = ''

        if reviews['receiverPhone'] is None:
            reviews['receiverPhone'] = ''

        if reviews['officeWar'] is None:
            reviews['officeWar'] = ''

        details.extend([reviews['orgFullName'],
                        reviews['orgEnName'],
                        reviews['orgCode'],
                        reviews['businessType'],
                        reviews['taxDate'],
                        reviews['taxCode'],
                        reviews['taxNation'],
                        codes[1],
                        reviews['statusOrg'],
                        reviews['agencyName'],
                        reviews['budgetCode'],
                        reviews['officeAdd'],
                        reviews['officePhone'],
                        reviews['officeWeb'],
                        reviews['repName'],
                        reviews['repPosition'],
                        reviews['repPhone'],
                        reviews['receiverPhone'],
                        reviews['officeWar']])

        if details[18] != '':
            ma = details[18]

            matinh = ma[:3]
            maquan = ma[:5]
            maphuong = ma

            for codeT in areaType1:
                if matinh == codeT[0]:
                    matinh = codeT[2]
            for codeQ in areaType2:
                if maquan == codeQ[0]:
                    maquan = codeQ[2]
            for codeH in areaType3:
                if maphuong == codeH[0]:
                    maphuong = codeH[2]
            if details[11] != '':
                company_address = details[11] + ', ' + maphuong + ', ' + maquan + ', ' + matinh
            else:
                company_address = maphuong + ', ' + maquan + ', ' + matinh
        else:
            if details[11] != '':
                company_address = details[11]
            else:
                company_address = None
        if details[0] != '':
            company_name = details[0]
        else:
            company_name = None

        if details[13] != '':
            company_website = details[13]
        else:
            company_website = None

        tax_code = details[5]

        if details[4] != '':
            operation_date = details[4]
        else:
            operation_date = None

        investor_is_approved = 1

        conn = connectdb.connect()

        cur = conn.cursor()
        sql = "SELECT id FROM pccc_app_job_company_profiles WHERE company_name = %s"
        val = (company_name,)
        cur.execute(sql, val)
        myresult = cur.fetchall()
        if myresult == []:
            status = 'Đã duyệt'
            sql = "INSERT INTO pccc_app_job_company_profiles (company_name, company_address, company_website, tax_code, operation_date, investor_is_approved,created_at,updated_at,status) VALUES (%s, %s, %s, %s, %s, %s, NOW(),NOW(), %s)"
            val = (
            company_name, company_address, company_website, tax_code, operation_date, investor_is_approved, status)
            cur.execute(sql, val)
            conn.commit()
        else:
            sql = "UPDATE pccc_app_job_company_profiles SET investor_is_approved = 1 WHERE company_name = %s"
            val = (company_name,)
            cur.execute(sql, val)
            conn.commit()

        with open('' + folder_path1 + '/benmoithau.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so ben moi thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so ben moi thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so ben moi thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so ben moi thau bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    return


def SoTrangTinTuc(startDay, endDay):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'MxgrKnHNN3-Xe22tsFannXdmvtuMYpnCU7UkbWt8.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1677124369938',
        '_ga_19996Z37EE': 'GS1.1.1677121319.27.1.1677124385.0.0.0',
        'citrix_ns_id': 'AAQ7yuD2YzvtbrUAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==pub2Yw==GsPDPtQJK8TMiTmbz--s9-ZDGSI=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=MxgrKnHNN3-Xe22tsFannXdmvtuMYpnCU7UkbWt8.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677124369938; _ga_19996Z37EE=GS1.1.1677121319.27.1.1677124385.0.0.0; citrix_ns_id=AAQ7yuD2YzvtbrUAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==pub2Yw==GsPDPtQJK8TMiTmbz--s9-ZDGSI=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    totalPageNumber = 0
    try:
        cookies = {
            'COOKIE_SUPPORT': 'true',
            'GUEST_LANGUAGE_ID': 'vi_VN',
            '_ga': 'GA1.1.2001033887.1675655198',
            'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
            '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
            '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
            '_ga_19996Z37EE': 'deleted',
            '_ga_19996Z37EE': 'deleted',
            'LFR_SESSION_STATE_20103': '1677219413221',
            'JSESSIONID': 'RfbEraKKRACZE9_9PpnKxo6-8zrHa-rVQ8-iuTPT.dc_app1_01',
            'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
            '_ga_19996Z37EE': 'GS1.1.1677217902.35.1.1677220398.0.0.0',
            'citrix_ns_id': 'AAE7r1T4YzsWXbcAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==wV34Yw==Fib7Z-IXoSfuyw_3_I380PiEz4k=',
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1677219413221; JSESSIONID=RfbEraKKRACZE9_9PpnKxo6-8zrHa-rVQ8-iuTPT.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1677217902.35.1.1677220398.0.0.0; citrix_ns_id=AAE7r1T4YzsWXbcAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==wV34Yw==Fib7Z-IXoSfuyw_3_I380PiEz4k=',
            'Origin': 'https://muasamcong.mpi.gov.vn',
            'Pragma': 'no-cache',
            'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
            'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = '{"pageSize":8,"pageNumber":"0","query":[{"index":"es-contractor-selection","keyWord":"","matchType":"all","matchFields":["notifyNo","bidName"],"filters":[{"fieldName":"publicDate","searchType":"range","from":"' + startDay + 'T00:00:00.000Z","to":"' + endDay + 'T23:59:59.059Z"}]}]}'
        response = requests.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/smart/search',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
        )
        json_data = response.json()
        reviews = json_data
        totalPageNumber = reviews['page']['totalPages']

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    return totalPageNumber


def CrawlMaTinTuc(pageNumber, codes, details, session1, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'LFR_SESSION_STATE_20103': '1677219413221',
        'JSESSIONID': 'RfbEraKKRACZE9_9PpnKxo6-8zrHa-rVQ8-iuTPT.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1677217902.35.1.1677220398.0.0.0',
        'citrix_ns_id': 'AAE7r1T4YzsWXbcAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==wV34Yw==Fib7Z-IXoSfuyw_3_I380PiEz4k=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1677219413221; JSESSIONID=RfbEraKKRACZE9_9PpnKxo6-8zrHa-rVQ8-iuTPT.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1677217902.35.1.1677220398.0.0.0; citrix_ns_id=AAE7r1T4YzsWXbcAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==wV34Yw==Fib7Z-IXoSfuyw_3_I380PiEz4k=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"pageSize":8,"pageNumber":"' + str(
            pageNumber) + '","query":[{"index":"es-contractor-selection","keyWord":"","matchType":"all","matchFields":["notifyNo","bidName"],"filters":[{"fieldName":"publicDate","searchType":"range","from":"' + startDay + 'T00:00:00.000Z","to":"' + endDay + 'T23:59:59.059Z"}]}]}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/smart/search',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data = response.json()
        reviews = json_data['page']['content']
        for review in reviews:
            if review['id'] is None:
                review['id'] = 0

            if review['stepCode'] is None:
                review['stepCode'] = 0

            if review['type'] is None:
                review['type'] = 0

            codes.append([review['id'], review['stepCode'], review['type']])

        for code in codes:
            if code[2] == 'es-plan-project-p':
                if code[1] == 'plan-step-1':
                    CrawlDetail_TT_KHLCNT(code=code[0], details=details, session1=session, codes=code,
                                          folder_path1=folder_path1)

            if code[2] == 'es-bidp-project-p':
                if code[1] == 'project-step-1':
                    CrawlDetail_TT_DA(code=code[0], details=details, session1=session, codes=code,
                                      folder_path1=folder_path1)

            if code[2] == 'es-notify-contractor':
                if code[1] == 'notify-contractor-step-1-tbmt':
                    CrawlDetail_TT_TBMT_CDT(code=code[0], details=details, session1=session, codes=code,
                                            folder_path1=folder_path1)

        codes.clear()

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    return


def CrawlDetail_TT_KHLCNT(code, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'l2FvcG6F98CG7gPz1NKaIJilQ2330njdj3-npPnB.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1677127244213',
        '_ga_19996Z37EE': 'GS1.1.1677121319.27.1.1677127264.0.0.0',
        'citrix_ns_id': 'AAU7Su72Yzs8cLUAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==8fH2Yw==R0m1YWb3n5ZJ5VCichrBk-NK6TM=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=l2FvcG6F98CG7gPz1NKaIJilQ2330njdj3-npPnB.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677127244213; _ga_19996Z37EE=GS1.1.1677121319.27.1.1677127264.0.0.0; citrix_ns_id=AAU7Su72Yzs8cLUAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==8fH2Yw==R0m1YWb3n5ZJ5VCichrBk-NK6TM=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-plan-project-p&stepCode=plan-step-1&id=332613e1-5466-4e7e-9b1e-8813082e77ae&notifyId=undefined&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=undefined&bidMode=undefined&notifyNo=undefined&planNo=PL2300019859&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bidp-plan-project-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data = response.json()
        data = json.dumps(json_data)

        if json_data is None:
            return
        else:
            if json_data['bidPoBidpPlanProjectDetailView'] is None:
                return
            else:
                review = json_data['bidPoBidpPlanProjectDetailView']
            if json_data['bidPoBidpPlanProjectDetailView'] is None:
                return
        nhap1 = [0]
        nhap1.clear()
        nhap = [0]
        nhap.clear()

        for gt in json_data['bidpPlanDetailToProjectList']:
            if gt['bidStartQuarter'] is None:
                gt['bidStartQuarter'] = ''

            if gt['bidStartMonth'] is None:
                gt['bidStartMonth'] = ''

            if gt['bidStartYear'] is None:
                gt['bidStartYear'] = ''

            if gt['bidStartUnit'] is None:
                gt['bidStartUnit'] = ''
            else:
                if gt['bidStartUnit'] == 'Q':
                    thoigian = str('Quý ') + str(gt['bidStartQuarter']) + ', ' + str(gt['bidStartYear'])
                elif gt['bidStartUnit'] == 'M':
                    thoigian = str('Tháng ') + str(gt['bidStartMonth']) + ', ' + str(gt['bidStartYear'])

            if gt['bidName'] is None:
                gt['bidName'] = ''

            if gt['bidField'] is None:
                gt['bidField'] = ''

            if gt['bidPrice'] is None:
                gt['bidPrice'] = ''

            if gt['capitalDetail'] is None:
                gt['capitalDetail'] = ''

            if gt['bidForm'] is None:
                gt['bidForm'] = ''
            else:
                if gt['bidForm'] == 'CHCT':
                    gt['bidForm'] = 'Chào hàng cạnh tranh'
                if gt['bidForm'] == 'DTRR':
                    gt['bidForm'] = 'Đấu thầu rộng rãi'
                if gt['bidForm'] == 'CHCTRG':
                    gt['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
                if gt['bidForm'] == 'CDTRG':
                    gt['bidForm'] = 'Chỉ định thầu rút gọn'

            if gt['bidMode'] is None:
                gt['bidMode'] = ''
            else:
                if gt['bidMode'] == '1_MTHS':
                    gt['bidMode'] = 'Một giai đoạn một túi hồ sơ'
                elif gt['bidMode'] == '1_HTHS':
                    gt['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

            if gt['ctype'] is None:
                gt['ctype'] = ''
            else:
                if gt['ctype'] == 'TG':
                    gt['ctype'] = 'Trọn gói'

            if gt['cperiod'] is None:
                gt['cperiod'] = ''

            if gt['cperiodUnit'] is None:
                gt['cperiodUnit'] = ''

            if gt['idDetail'] is None:
                gt['idDetail'] = ''

            if gt['isDomestic'] is None:
                gt['isDomestic'] = ''
            else:
                if gt['isDomestic'] == 1:
                    gt['isDomestic'] = 'Trong nước'
                elif gt['isDomestic'] == 0:
                    gt['isDomestic'] = 'Quốc tế'

            if gt['isInternet'] is None:
                gt['isInternet'] = ''
            else:
                if gt['isInternet'] == 1:
                    gt['isInternet'] = 'Qua mạng'
                elif gt['isInternet'] == 0:
                    gt['isInternet'] = 'Không qua mạng'

            if gt['isPrequalification'] is None:
                gt['isPrequalification'] = ''
            else:
                if gt['isPrequalification'] == 1:
                    gt['isPrequalification'] = 'Có sơ tuyển'
                elif gt['isPrequalification'] == 0:
                    gt['isPrequalification'] = 'Không sơ tuyển'

            nhap.append([gt['bidName'],
                         gt['bidField'],
                         gt['bidPrice'],
                         gt['capitalDetail'],
                         gt['bidForm'],
                         gt['bidMode'],
                         thoigian,
                         gt['ctype'],
                         str(gt['cperiod']) + str(gt['cperiodUnit']),
                         gt['idDetail'],
                         gt['isDomestic'],
                         gt['isInternet'],
                         gt['isPrequalification']])

        for nhapy in nhap:
            nhapx = CrawlDetail_TT_KHLCNT_1(code=nhapy[9], session1=session, folder_path1=folder_path1)
            nhap1.append(nhapx)

        if review['planNo'] is None:
            review['planNo'] = ''

        if review['pname'] is None:
            review['pname'] = ''

        if review['name'] is None:
            review['name'] = ''

        if review['investTarget'] is None:
            review['investTarget'] = ''

        if review['investorName'] is None:
            review['investorName'] = ''

        if review['bidPack'] is None:
            review['investorName'] = ''

        if review['pperiodUnit'] is not None:
            if review['pperiodUnit'] == 1:
                review['pperiodUnit'] = 'Năm'
            if review['pperiodUnit'] == 2:
                review['pperiodUnit'] = 'Tháng'
            if review['pperiodUnit'] == 3:
                review['pperiodUnit'] = 'Ngày'
        else:
            review['pperiodUnit'] = ''

        if review['pperiod'] is None:
            review['pperiod'] = ''

        if review['pgroup'] is None:
            review['pgroup'] = ''

        if review['pform'] is None:
            review['pform'] = ''

        if review['isOda'] is None:
            review['isOda'] = ''
        else:
            if review['isOda'] is False:
                review['isOda'] = 'Không'
            else:
                review['isOda'] = 'Có'

        if review['location'] is None:
            review['location'] = ''

        if review['investTotal'] is None:
            review['investTotal'] = ''

        if review['decisionNo'] is None:
            review['decisionNo'] = ''

        if review['decisionDate'] is None:
            review['decisionDate'] = ''
        else:
            # Tạo đối tượng datetime từ chuỗi thời gian ban đầu
            review['decisionDate'] = datetime.fromisoformat(review['decisionDate'])

            # Chuyển đổi đối tượng datetime sang chuỗi ngày tháng mong muốn
            review['decisionDate'] = review['decisionDate'].strftime('%Y/%m/%d')
            review['decisionDate'] = review['decisionDate'] + ' 00:00:00'
        if review['decisionAgency'] is None:
            review['decisionAgency'] = ''

        if review['planVersion'] is None:
            review['planVersion'] = ''

        if review['publicDate'] is None:
            review['publicDate'] = ''
        else:
            review['publicDate'] = review['publicDate'][:19]
            # Tạo đối tượng datetime từ chuỗi thời gian ban đầu
            review['publicDate'] = datetime.strptime(review['publicDate'], '%Y-%m-%dT%H:%M:%S')

            # Chuyển đổi đối tượng datetime sang chuỗi ngày tháng mong muốn
            review['publicDate'] = review['publicDate'].strftime('%Y-%m-%d %H:%M:%S')

        if review['planType'] is None:
            review['planType'] = ''

        if review['decisionFileId'] is None:
            review['decisionFileId'] = ''
            link = ''
        else:
            link = 'http://localhost:1234/api/download/file/browser/public?fileId=' + review['decisionFileId']

        if review['decisionFileName'] is None:
            review['decisionFileName'] = ''

        a = 0

        details.extend([review['planNo'],
                        review['name'],
                        review['planVersion'],
                        review['pname'],
                        review['investTarget'],
                        review['investorName'],
                        review['bidPack'],
                        str(review['pperiod']) + str(review['pperiodUnit']),
                        review['pgroup'],
                        review['pform'],
                        review['isOda'],
                        review['location'],
                        review['investTotal'],
                        review['decisionNo'],
                        review['decisionDate'],
                        review['decisionAgency'],
                        a,
                        nhap,
                        nhap1,
                        codes,
                        review['publicDate'],
                        review['planType'],
                        review['decisionFileName'],
                        link])

        upData_KHLCNT(details=details)

        with open('' + folder_path1 + '/KHLCNT.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so KHLCNT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.exceptions.ConnectionError as err :
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so KHLCNT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so KHLCNT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so KHLCNT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass
    return


def upData_KHLCNT(details):
    bid_number = str(details[0])
    bid_turn_no = str(details[2])
    ten_chu_dau_tu = details[5].replace('\n', '').replace('\t', '')

    conn = connectdb.connect()
    cur = conn.cursor()
    sql = "SELECT id FROM pccc_app_job_company_profiles WHERE company_name = %s"
    val = (ten_chu_dau_tu,)
    cur.execute(sql, val)
    conn.commit()
    myresult = cur.fetchone()
    if myresult:
        subject_id_1 = myresult[0]
        subject_id_1 = str(subject_id_1)
        subject_type_1 = 'App\Models\JobCompanyProfile'
    else:
        subject_id_1 = None
        subject_type_1 = None

    sql = "SELECT * FROM pccc_app_bidding_news WHERE type_id = 1 AND bid_number = %s AND bid_turn_no = %s"
    val = (bid_number, bid_turn_no)
    cur.execute(sql, val)
    conn.commit()
    myresult = cur.fetchall()

    if myresult == []:
        time_posting = details[20]
        # Chuyển đổi sang đối tượng datetime
        # dt_obj = datetime.fromisoformat(dt_str)
        # Format lại theo định dạng mong muốn
        # time_posting = dt_obj.strftime("%Y-%m-%d %H:%M:%S")

        date_of_approval = details[14]
        # input_format = "%Y-%m-%dT%H:%M:%S"
        # output_format = "%Y-%m-%d %H:%M:%S"

        # datetime_obj = datetime.strptime(input_str, input_format)
        # date_of_approval = datetime_obj.strftime(output_format)

        sql = "INSERT INTO pccc_app_bidding_news (type_id, created_at, updated_at,bid_number,bid_turn_no,time_posting,date_of_approval) VALUES (1,NOW(),NOW(),%s,%s,%s,%s)"
        val = (bid_number, bid_turn_no, time_posting, date_of_approval)
        cur.execute(sql, val)
        conn.commit()

        news_id = cur.lastrowid
        news_id = int(news_id)
        type_id = 1

        sub_title = 'THÔNG TIN CHI TIẾT'

        khlcnt_number = details[0]

        so_khlcnt = str(khlcnt_number) + ' - ' + str(bid_turn_no)

        loai_thong_bao = 'Thông báo thực'

        if bid_turn_no == 00 or bid_turn_no == '00':
            hinh_thuc_thong_bao = 'Đăng lần đầu'
        else:
            hinh_thuc_thong_bao = 'Thay đổi'

        ten_khlcnt = details[1].replace('\n', '').replace('\t', '')

        ten_chu_dau_tu = details[5].replace('\n', '').replace('\t', '')

        pham_vi_dieu_chinh = ''

        trang_thai_quyet_dinh = ''

        ngay_phe_duyet_khlcnt = details[14]

        so_qd_phe_duyet_khlcnt = details[13]

        if details[12] != '':
            tong_muc_dau_tu = int(details[12])
            tong_muc_dau_tu = "{:,}".format(tong_muc_dau_tu).replace(",", ".") + " VND"

        else:
            tong_muc_dau_tu = details[12]

        ngay_dang_tai = time_posting

        thong_bao_lien_quan = ''

        quyet_dinh_phe_duyet = None

        if details[21] == 'DTPT':

            titles1 = 'Số KHLCNT'

            titles2 = 'Loại thông báo'

            titles3 = 'Hình thức thông báo'

            titles4 = 'Tên KHLCNT'

            titles5 = 'Tên chủ đầu tư'

            titles6 = 'Phân loại'

            titles7 = 'Phạm vi điều chỉnh'

            titles8 = 'Trạng thái quyết định'

            titles9 = 'Ngày phê duyệt KHLCNT'

            titles10 = 'Số QĐ phê duyệt KHLCNT'

            titles11 = 'Tổng mức đầu tư'

            titles12 = 'Ngày đăng tải'

            titles13 = 'Thông báo liên quan'

            titles14 = 'Quyết định phê duyệt'

            phan_loai = 'Dự án đầu tư phát triển'

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

            value1 = so_khlcnt

            value2 = loai_thong_bao

            value3 = hinh_thuc_thong_bao

            value4 = ten_khlcnt

            value5 = ten_chu_dau_tu

            value6 = phan_loai

            value7 = pham_vi_dieu_chinh

            value8 = trang_thai_quyet_dinh

            value9 = ngay_phe_duyet_khlcnt

            value10 = so_qd_phe_duyet_khlcnt

            value11 = tong_muc_dau_tu

            value12 = ngay_dang_tai

            value13 = thong_bao_lien_quan

            value14 = quyet_dinh_phe_duyet

            subject_id = None
            subject_type = None

            records = [
                (key1, sub_title, titles1, value1, subject_id, subject_type, news_id, type_id),
                (key2, sub_title, titles2, value2, subject_id, subject_type, news_id, type_id),
                (key3, sub_title, titles3, value3, subject_id, subject_type, news_id, type_id),
                (key4, sub_title, titles4, value4, subject_id, subject_type, news_id, type_id),
                (key5, sub_title, titles5, value5, subject_id_1, subject_type_1, news_id, type_id),
                (key6, sub_title, titles6, value6, subject_id, subject_type, news_id, type_id),
                (key7, sub_title, titles7, value7, subject_id, subject_type, news_id, type_id),
                (key8, sub_title, titles8, value8, subject_id, subject_type, news_id, type_id),
                (key9, sub_title, titles9, value9, subject_id, subject_type, news_id, type_id),
                (key10, sub_title, titles10, value10, subject_id, subject_type, news_id, type_id),
                (key11, sub_title, titles11, value11, subject_id, subject_type, news_id, type_id),
                (key12, sub_title, titles12, value12, subject_id, subject_type, news_id, type_id),
                (key13, sub_title, titles13, value13, subject_id, subject_type, news_id, type_id),
                (key14, sub_title, titles14, value14, subject_id, subject_type, news_id, type_id)]

            sql1 = "INSERT INTO pccc_app_bidding_news_details (`key`, sub_title, title, value, subject_id, subject_type, news_id, type_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW());"
            cur.executemany(sql1, records)
            conn.commit()

        else:

            titles1 = 'Số KHLCNT'

            titles2 = 'Loại thông báo'

            titles3 = 'Hình thức thông báo'

            titles4 = 'Tên KHLCNT'

            titles5 = 'Bên mời thầu'

            titles6 = 'Phân loại'

            titles7 = 'Phạm vi điều chỉnh'

            # titles8 = 'Trạng thái quyết định'

            titles9 = 'Ngày phê duyệt KHLCNT'

            titles10 = 'Số QĐ phê duyệt KHLCNT'

            titles11 = 'Giá dự toán'

            titles12 = 'Ngày đăng tải'

            titles13 = 'Thông báo liên quan'

            titles14 = 'Quyết định phê duyệt'

            phan_loai = 'Hoạt động chi thường xuyên'

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

            # key8=titles8.strip().lower().replace(' ', '-')
            # key8 = unidecode(key8)

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

            value1 = so_khlcnt

            value2 = loai_thong_bao

            value3 = hinh_thuc_thong_bao

            value4 = ten_khlcnt

            value5 = ten_chu_dau_tu

            value6 = phan_loai

            value7 = pham_vi_dieu_chinh

            # value8 = trang_thai_quyet_dinh

            value9 = ngay_phe_duyet_khlcnt

            value10 = so_qd_phe_duyet_khlcnt

            value11 = tong_muc_dau_tu

            value12 = ngay_dang_tai

            value13 = thong_bao_lien_quan

            value14 = quyet_dinh_phe_duyet

            subject_id = None
            subject_type = None

            records = [
                (key1, sub_title, titles1, value1, subject_id, subject_type, news_id, type_id),
                (key2, sub_title, titles2, value2, subject_id, subject_type, news_id, type_id),
                (key3, sub_title, titles3, value3, subject_id, subject_type, news_id, type_id),
                (key4, sub_title, titles4, value4, subject_id, subject_type, news_id, type_id),
                (key5, sub_title, titles5, value5, subject_id_1, subject_type_1, news_id, type_id),
                (key6, sub_title, titles6, value6, subject_id, subject_type, news_id, type_id),
                (key7, sub_title, titles7, value7, subject_id, subject_type, news_id, type_id),

                (key9, sub_title, titles9, value9, subject_id, subject_type, news_id, type_id),
                (key10, sub_title, titles10, value10, subject_id, subject_type, news_id, type_id),
                (key11, sub_title, titles11, value11, subject_id, subject_type, news_id, type_id),
                (key12, sub_title, titles12, value12, subject_id, subject_type, news_id, type_id),
                (key13, sub_title, titles13, value13, subject_id, subject_type, news_id, type_id),
                (key14, sub_title, titles14, value14, subject_id, subject_type, news_id, type_id)]

            sql1 = "INSERT INTO pccc_app_bidding_news_details (`key`, sub_title, title, value, subject_id, subject_type, news_id, type_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW());"
            cur.executemany(sql1, records)
            conn.commit()

        id_news_detail_file = cur.lastrowid
        object_id = id_news_detail_file

        file_name = details[22]

        link_file = details[23]

        object_type = 'App\Models\BiddingNewsDetail'

        is_big_file = 1

        sql = "INSERT INTO pccc_app_bidding_news_files (object_type, object_id, file_name, link_muasamcong, created_at, updated_at, is_big_file) VALUES (%s, %s, %s, %s, NOW(), NOW(), %s) "
        val = (object_type, object_id, file_name, link_file, is_big_file)
        cur.execute(sql, val)
        conn.commit()

        for tbmt in details[18]:
            lcnt_field = tbmt[4]
            package_name = tbmt[1].replace('\n', '').replace('\t', '')
            package_name = package_name[:191]

            bid_price = tbmt[13]
            bid_price = '{:,}'.format(bid_price).replace(',', '.')

            capital_detail = tbmt[9].replace('\n', '').replace('\t', '')
            capital_detail = capital_detail[:191]

            form_of_lcnt = tbmt[6] + ', ' + tbmt[3].lower() + ' ' + tbmt[5].lower() + ', ' + tbmt[2].lower()
            lcnt_method = tbmt[7]
            time_start_lcnt = tbmt[11]
            contract_type = tbmt[8]
            duration_of_contact = tbmt[12]
            execution_address = tbmt[14]
            number_tbml_tbmst = tbmt[15]

            sql = "INSERT INTO pccc_app_bidding_plan_package (news_id, lcnt_field, package_name, bid_price, capital_detail, form_of_lcnt, lcnt_method, time_start_lcnt, contract_type, duration_of_contract, created_at, updated_at, execution_address, number_tbml_tbmst) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s)"
            val = (
            news_id, lcnt_field, package_name, bid_price, capital_detail, form_of_lcnt, lcnt_method, time_start_lcnt,
            contract_type, duration_of_contact, execution_address, number_tbml_tbmst)
            cur.execute(sql, val)
            conn.commit()

    else:
        return


def CrawlDetail_TT_KHLCNT_1(code, session1, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 't7pL8my1iOlIZcqsFi0FJ63hVshRerZ1A5uwrHcW.dc_app1_02',
        '_ga_19996Z37EE': 'GS1.1.1678160637.78.1.1678162323.0.0.0',
        'LFR_SESSION_STATE_20103': '1678162332373',
        'citrix_ns_id': 'AAQ7-rIGZDsbKssAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==I70GZA==rmqf_FqnXDNNeAfnlWL99RpxLaE=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=t7pL8my1iOlIZcqsFi0FJ63hVshRerZ1A5uwrHcW.dc_app1_02; _ga_19996Z37EE=GS1.1.1678160637.78.1.1678162323.0.0.0; LFR_SESSION_STATE_20103=1678162332373; citrix_ns_id=AAQ7-rIGZDsbKssAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==I70GZA==rmqf_FqnXDNNeAfnlWL99RpxLaE=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-plan-project-p&stepCode=plan-step-1&id=15196cdb-7d9b-4afa-a86c-c523f5df3cb6&notifyId=undefined&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=undefined&bidMode=undefined&notifyNo=undefined&planNo=PL2300026100&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/lcnt/bid-po-bidp-plan-project-view/get-bidp-plan-detail-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        reviews = response.json()

        if reviews is None:
            return

        if reviews['processApply'] is None:
            reviews['processApply'] = ''

        if reviews['bidName'] is None:
            reviews['bidName'] = ''

        if reviews['isInternet'] is None:
            reviews['isInternet'] = ''
        else:
            if reviews['isInternet'] == 1:
                reviews['isInternet'] = 'Qua mạng'
            elif reviews['isInternet'] == 0:
                reviews['isInternet'] = 'Không qua mạng'

        if reviews['isDomestic'] is None:
            reviews['isDomestic'] = ''
        else:
            if reviews['isDomestic'] == 1:
                reviews['isDomestic'] = 'Trong nước'
            elif reviews['isDomestic'] == 0:
                reviews['isDomestic'] = 'Quốc tế'

        if reviews['bidField'] is None:
            reviews['bidField'] = ''
        else:
            if reviews['bidField'] == 'XL':
                reviews['bidField'] = 'Xây lắp'
            elif reviews['bidField'] == 'TV':
                reviews['bidField'] = 'Tư vấn'
            elif reviews['bidField'] == 'PTV':
                reviews['bidField'] = 'Phi tư vấn'
            elif reviews['bidField'] == 'HH':
                reviews['bidField'] = 'Hàng hóa'

        if reviews['isPrequalification'] is None:
            reviews['isPrequalification'] = ''
        else:
            if reviews['isPrequalification'] == 0:
                reviews['isPrequalification'] = 'Không'
            elif reviews['isPrequalification'] == 1:
                reviews['isPrequalification'] = 'Có'
        bidForm = ''

        if reviews['bidForm'] is None:
            reviews['bidForm'] = ''
            bidForm = ''
        else:
            if reviews['bidForm'] == 'CHCT':
                bidForm = 'Chào hàng cạnh tranh'
            if reviews['bidForm'] == 'DTRR':
                bidForm = 'Đấu thầu rộng rãi'
            if reviews['bidForm'] == 'CHCTRG':
                bidForm = 'Chào hàng cạnh tranh rút gọn'
            if reviews['bidForm'] == 'CDTRG':
                bidForm = 'Chỉ định thầu rút gọn'

        if reviews['bidMode'] is None:
            reviews['bidMode'] = ''
        else:
            if reviews['bidMode'] == '1_MTHS':
                reviews['bidMode'] = 'Một giai đoạn một túi hồ sơ'
            elif reviews['bidMode'] == '1_HTHS':
                reviews['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

        if reviews['ctype'] is None:
            reviews['ctype'] = ''
        else:
            if reviews['ctype'] == 'TG':
                reviews['ctype'] = 'Trọn gói'

        if reviews['capitalDetail'] is None:
            reviews['capitalDetail'] = ''

        if reviews['isConcentrateShopping'] is None:
            reviews['isConcentrateShopping'] = ''
        else:
            if reviews['isConcentrateShopping'] == 1:
                reviews['isConcentrateShopping'] = 'Có'
            else:
                reviews['isConcentrateShopping'] = 'Không'

        if reviews['bidStartYear'] is None:
            reviews['bidStartYear'] = ''
        if reviews['bidStartQuarter'] is None:
            reviews['bidStartQuarter'] = ''
        if reviews['bidStartMonth'] is None:
            reviews['bidStartMonth'] = ''
        thoigian = ''
        if reviews['bidStartUnit'] is None:
            reviews['bidStartUnit'] = ''
        else:
            if reviews['bidStartUnit'] == 'Q':
                reviews['bidStartUnit'] = 'Quý'
                thoigian = str(reviews['bidStartUnit']) + ' ' + str(reviews['bidStartQuarter']) + ', ' + str(
                    reviews['bidStartYear'])
            elif reviews['bidStartUnit'] == 'M':
                reviews['bidStartUnit'] = 'Tháng'
                thoigian = str(reviews['bidStartUnit']) + ' ' + str(reviews['bidStartMonth']) + ', ' + str(
                    reviews['bidStartYear'])

        if reviews['cperiod'] is None:
            reviews['cperiod'] = ''
        if reviews['cperiodUnit'] is None:
            reviews['cperiodUnit'] = ''
        else:
            if reviews['cperiodUnit'] == 'D':
                reviews['cperiodUnit'] = str(reviews['cperiod']) + ' ' + 'ngày'
            elif reviews['cperiodUnit'] == 'M':
                reviews['cperiodUnit'] = str(reviews['cperiod']) + ' ' + 'tháng'

        if reviews['bidPrice'] is None:
            reviews['bidPrice'] = ''

        diadiem = ''

        if reviews['bidLocation'] is None:
            reviews['bidLocation'] = ''
        else:
            if reviews['bidLocation'] == []:
                diadiem = ''
            else:
                if reviews['bidLocation'][0] is None:
                    reviews['bidLocation'][0] = ''
                else:
                    if reviews['bidLocation'][0]['districtName'] is None:
                        if reviews['bidLocation'][0]['provName'] is None:
                            diadiem = ''
                        else:
                            diadiem = str(reviews['bidLocation'][0]['provName'])
                    else:
                        diadiem = str(reviews['bidLocation'][0]['districtName']) + ', ' + str(
                            reviews['bidLocation'][0]['provName'])

        if reviews['bidNo'] is None:
            reviews['bidNo'] = ''

        nhap1 = []
        nhap1.clear()
        nhap1.extend([reviews['processApply'],
                      reviews['bidName'],
                      reviews['isInternet'],
                      reviews['isDomestic'],
                      reviews['bidField'],
                      reviews['isPrequalification'],
                      bidForm,
                      reviews['bidMode'],
                      reviews['ctype'],
                      reviews['capitalDetail'],
                      reviews['isConcentrateShopping'],
                      thoigian,
                      reviews['cperiodUnit'],
                      reviews['bidPrice'],
                      diadiem,
                      reviews['bidNo']])
        return nhap1

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so thong tin goi thau trong KHLCNT bi loi khong lay duoc du lieu : " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so thong tin goi thau trong KHLCNT bi loi khong lay duoc du lieu : " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so thong tin goi thau trong KHLCNT bi loi khong lay duoc du lieu : " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so thong tin goi thau trong KHLCNT bi loi khong lay duoc du lieu : " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass


def CrawlDetail_TT_TBMT_CDT(code, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'QSxMI7S0nMCiI0UxzJ6_tsd-u_OJZ28Zb-HBnJkL.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1677131363227',
        '_ga_19996Z37EE': 'GS1.1.1677130916.28.1.1677131407.0.0.0',
        'citrix_ns_id': 'AAE7o_z2YzsSNrQAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==JQL3Yw==xzwqHBiMJQ5vayk1QLkWIfwcuvs=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=QSxMI7S0nMCiI0UxzJ6_tsd-u_OJZ28Zb-HBnJkL.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677131363227; _ga_19996Z37EE=GS1.1.1677130916.28.1.1677131407.0.0.0; citrix_ns_id=AAE7o_z2YzsSNrQAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==JQL3Yw==xzwqHBiMJQ5vayk1QLkWIfwcuvs=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-1-tbmt&id=c3c91820-53d0-4b2d-92af-c180662f55dd&notifyId=c3c91820-53d0-4b2d-92af-c180662f55dd&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300021826&planNo=PL2300010712&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bido-notify-contractor-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data = response.json()
        if json_data is None:
            return
        data = json.dumps(json_data)

        if data.find('bidoNotifyContractorP') != -1:
            if json_data['bidoNotifyContractorP'] is not None:
                review = json_data['bidoNotifyContractorP']

                if review['cPeriod'] is None:
                    review['cPeriod'] = ''

                if review['cPeriodUnit'] is None:
                    review['cPeriodUnit'] = ''

                a = str(review['cPeriod']) + str(review['cPeriodUnit'])

                if review['cType'] is None:
                    review['cType'] = ''
                else:
                    v = review['cType']

        elif data.find('bidoNotifyContractorM') != -1:
            if json_data['bidoNotifyContractorM'] is None:
                return
            else:
                review = json_data['bidoNotifyContractorM']

            if review['contractPeriod'] is None:
                review['contractPeriod'] = ''

            if review['contractPeriodUnit'] is None:
                review['contractPeriodUnit'] = ''

            a = str(review['contractPeriod']) + str(review['contractPeriodUnit'])

            if review['contractType'] is None:
                review['contractType'] = ''
            else:
                v = review['contractType']

        if review['notifyNo'] is None:
            review['notifyNo'] = ''

        if review['publicDate'] is None:
            review['publicDate'] = ''

        if review['planNo'] is None:
            review['planNo'] = ''

        if review['planType'] is None:
            review['planType'] = ''
        else:
            if review['planType'] == 'DTPT':
                review['planType'] = 'Chi đầu tư phát triển'
            elif review['planType'] == 'TX':
                review['planType'] = 'Chi thường xuyên'

        if review['planName'] is None:
            review['planName'] = ''

        if review['bidName'] is None:
            review['bidName'] = ''

        if review['investorName'] is None:
            review['investorName'] = ''

        if review['procuringEntityName'] is None:
            review['procuringEntityName'] = ''

        if review['capitalDetail'] is None:
            review['capitalDetail'] = ''

        if review['investField'] is None:
            review['investField'] = ''
        else:
            if review['investField'] == 'XL':
                review['investField'] = 'Xây lắp'
            elif review['investField'] == 'TV':
                review['investField'] = 'Tư vấn'
            elif review['investField'] == 'PTV':
                review['investField'] = 'Phi tư vấn'
            elif review['investField'] == 'HH':
                review['investField'] = 'Hàng hóa'

        bidForm = ''
        if review['bidForm'] is None:
            review['bidForm'] = ''
        else:
            if review['bidForm'] == 'CHCT':
                bidForm = 'Chào hàng cạnh tranh'
            if review['bidForm'] == 'DTRR':
                bidForm = 'Đấu thầu rộng rãi'
            if review['bidForm'] == 'CHCTRG':
                bidForm = 'Chào hàng cạnh tranh rút gọn'
            if review['bidForm'] == 'CDTRG':
                bidForm = 'Chỉ định thầu rút gọn'

        if review['isDomestic'] is None:
            review['isDomestic'] = ''
        else:
            if review['isDomestic'] == 1:
                review['isDomestic'] = 'Trong nước'
            elif review['isDomestic'] == 0:
                review['isDomestic'] = 'Quốc tế'

        if review['bidMode'] is None:
            review['bidMode'] = ''
        else:
            if review['bidMode'] == '1_MTHS':
                review['bidMode'] = 'Một giai đoạn một túi hồ sơ'
            elif review['bidMode'] == '1_HTHS':
                review['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

        if review['isInternet'] is None:
            review['isInternet'] = ''
        else:
            if review['isInternet'] == 1:
                review['isInternet'] = 'Qua mạng'
            elif review['isInternet'] == 0:
                review['isInternet'] = 'Không qua mạng'

        if review['issueLocation'] is None:
            review['issueLocation'] = ''

        fee = ''
        if review['isInternet'] == 1:
            if review['bidForm'] == 'DTRR' or review['bidForm'] == 'DTHC' or review['bidForm'] == 'MSTT':
                fee = '330,000 VND'
            elif review['bidForm'] == 'CHCT' or review['bidForm'] == 'CHCTRG':
                fee = '220,000 VND'
        elif review['isInternet'] == 0:
            if review['feeValue'] is None:
                fee = ''
            else:
                fee = str(review['feeValue']) + ' VND'

        if review['receiveLocation'] is None:
            review['receiveLocation'] = ''

        b = ''
        if data.find('bidpBidLocationList') != -1:
            if json_data['bidpBidLocationList'] is None or json_data['bidpBidLocationList'] == []:
                b = ''
            else:
                if json_data['bidpBidLocationList'][0] is not None or json_data['bidpBidLocationList'][0] != []:
                    if json_data['bidpBidLocationList'][0]['districtName'] is None:
                        b = json_data['bidpBidLocationList'][0]['provName']
                    elif json_data['bidpBidLocationList'][0]['provName'] is None:
                        b = json_data['bidpBidLocationList'][0]['districtName']
                    else:
                        b = json_data['bidpBidLocationList'][0]['districtName'] + ", " + \
                            json_data['bidpBidLocationList'][0]['provName']

        elif data.find('lsBidpBidLocationDTO') != -1:
            if json_data['lsBidpBidLocationDTO'] is not None or json_data['lsBidpBidLocationDTO'] != []:
                if json_data['lsBidpBidLocationDTO'][0] is not None or json_data['lsBidpBidLocationDTO'][0] != []:
                    if json_data['lsBidpBidLocationDTO'][0]['districtName'] is None:
                        b = json_data['lsBidpBidLocationDTO'][0]['provName']
                    elif json_data['lsBidpBidLocationDTO'][0]['provName'] is None:
                        b = json_data['lsBidpBidLocationDTO'][0]['districtName']
                    else:
                        b = json_data['lsBidpBidLocationDTO'][0]['districtName'] + ", " + \
                            json_data['lsBidpBidLocationDTO'][0]['provName']

        if review['bidCloseDate'] is None:
            review['bidCloseDate'] = ''

        if review['bidOpenDate'] is None:
            review['bidOpenDate'] = ''

        if review['bidOpenLocation'] is None:
            review['bidOpenLocation'] = ''

        if review['bidValidityPeriod'] is None:
            review['bidValidityPeriod'] = ''

        if review['bidValidityPeriodUnit'] is None:
            review['bidValidityPeriodUnit'] = ''
        x = str(review['bidValidityPeriod']) + ' ' + str(review['bidValidityPeriodUnit'])

        if review['guaranteeValue'] is None:
            review['guaranteeValue'] = ''

        if review['guaranteeForm'] is None:
            review['guaranteeForm'] = ''

        decisionNo = ''
        if data.find('bidInvContractorOfflineDTO') != -1:
            if json_data['bidInvContractorOfflineDTO'] is not None:
                if json_data['bidInvContractorOfflineDTO']['decisionNo'] is not None:
                    decisionNo = json_data['bidInvContractorOfflineDTO']['decisionNo']

                if json_data['bidInvContractorOfflineDTO']['decisionDate'] is None:
                    json_data['bidInvContractorOfflineDTO']['decisionDate'] = ''
                else:
                    input_date = json_data['bidInvContractorOfflineDTO']['decisionDate']
                    input_date= input_date[:19]
                    date_obj = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S")
                    formatted_date = date_obj.strftime("%d/%m/%Y")

                if json_data['bidInvContractorOfflineDTO']['decisionAgency'] is None:
                    decisionAgency = ''
                else:
                    decisionAgency = json_data['bidInvContractorOfflineDTO']['decisionAgency']
                if json_data['bidInvContractorOfflineDTO']['decisionFileName'] is None:
                    json_data['bidInvContractorOfflineDTO']['decisionFileName'] = ''
                else:
                    decisionFileName = json_data['bidInvContractorOfflineDTO']['decisionFileName']
                if json_data['bidInvContractorOfflineDTO']['decisionFileId'] is None:
                    json_data['bidInvContractorOfflineDTO']['decisionFileId'] = ''
                else:
                    link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + str(
                        json_data['bidInvContractorOfflineDTO']['decisionFileId'])
        link2 = ''
        if review['id'] is None:
            link2 = ''
        else:
            if review['isInternet'] == 1 or review['isInternet'] == 'Qua mạng':
                link2 = 'https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=' + str(review['id'])

        listHangHoa = []
        listHangHoa.clear()
        check_listHH = None
        if review['investField'] == 'Hàng hóa' or review['investField'] == 'HH':
            listx, check_listHH = crawlDetail_HangHoa(data=json_data)
            listHangHoa.extend(listx)

        listFileDinhKemHSMT = []
        listFileDinhKemHSMT.clear()
        if json_data['bidoInvBiddingDTO'] is not None:
            if json_data['bidoInvBiddingDTO'] != []:
                listz=crawlDetail_FileDinhKemHSMT(data=json_data['bidoInvBiddingDTO'])
                listFileDinhKemHSMT.extend(listz)

        listFileHSMT = []
        listFileHSMT.clear()
        list_file = []
        if review['isInternet'] == 'Qua mạng' or review['isInternet'] == '1' or review['isInternet'] == 1:
            list_file = []
            list_file.clear()
            if json_data is not None:
                stt = ''
                if json_data['bidaInvChapterConfList'] is None or json_data['bidaInvChapterConfList'] == []:
                    listFileHSMT = []
                else:
                    reviewx = json_data['bidaInvChapterConfList']
                    sttpcode1 = 0
                    sttpcode2 = 20
                    sttpcode3 = 40
                    stt = 0
                    list_file = []
                    list_file.clear()

                    for review1 in reviewx:
                        if review1['lev'] is not None:
                            if review1['lev'] <= 1:
                                idFile = review['id']
                                lev = review1['lev']
                                code1 = review1['code']

                                if review1['pcode'] is None:
                                    pcode = ''
                                else:
                                    pcode = review1['pcode']
                                name = review1['name']
                                orderIndex = review1['orderIndex']
                                if lev == 0:
                                    if orderIndex == 0:
                                        stt = sttpcode1

                                    if orderIndex == 1:
                                        stt = sttpcode2

                                    if orderIndex == 2:
                                        stt = sttpcode3

                                if lev == 1:
                                    if pcode == 'P1':
                                        stt = orderIndex + sttpcode1 + 1

                                    if pcode == 'P2':
                                        stt = orderIndex + sttpcode2 + 1

                                    if pcode == 'P3':
                                        stt = orderIndex + sttpcode3 + 1

                                list_file.append([stt, idFile, lev, name, code1, pcode, orderIndex])
                    
            
        if list_file is None or list_file == []:
            listFileHSMT = []
        else:
            listFileHSMT = []
            listFileHSMT.clear()
            listFileHSMT = sorted(list_file, key=lambda list_file: list_file[0])

        if review['bidPrice'] is None:
            review['bidPrice'] = ''

        if review['notifyVersion'] is None:
            review['notifyVersion'] = ''

        details.extend([review['notifyNo'],#0
                        review['publicDate'],#1
                        review["notifyVersion"],#2
                        review['planNo'],#3
                        review['planType'],#4
                        review['planName'],#5
                        review['bidName'],#6
                        review['investorName'],#7
                        review['procuringEntityName'],#8
                        review['capitalDetail'],#9
                        review['investField'],#10
                        bidForm,#11
                        v,#12
                        review['isDomestic'],#13
                        review['bidMode'],#14
                        a,#15
                        review['isInternet'],#16
                        review['issueLocation'],#17
                        fee,#18
                        review['receiveLocation'],#19
                        b,#20
                        review['bidCloseDate'],#21
                        review['bidOpenDate'],#22
                        review['bidOpenLocation'],#23
                        x,#24
                        review['guaranteeValue'],#25
                        review['bidPrice'],#26
                        review['guaranteeForm'],#27
                        decisionNo,#28
                        formatted_date,#29
                        decisionAgency,#30
                        link1,#31
                        link2,#32
                        codes,#33
                        listHangHoa,#34
                        listFileHSMT,#35
                        decisionFileName,#36
                        listFileDinhKemHSMT,
                        check_listHH])#37

        bidType = upABN_db.bid_type(details[10])
        bidMethod = upABN_db.bid_method(details[16])
        crea_at = upABN_db.timeUpd()
        tim_close = upABN_db.time_close(details[21])
        time_post = upABN_db.time_post(details[1])
        date_app = upABN_db.date_app(formatted_date)
        news_id = 0

        if upABN_db.ktTrungDL(review['notifyNo'], review["notifyVersion"]) == None:

            news_id = upABN_db.upDataDB(3, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'],
                                        review["notifyVersion"],
                                        tim_close, time_post, date_app)

            upABNDetail_db.upData(details, news_id)

            conn = connectdb.connect()
            cur = conn.cursor()
            sql = "SELECT * FROM pccc_app_bidding_news_details WHERE `key` = %s AND news_id = %s"
            val = ('ho-so-moi-thau', news_id)
            cur.execute(sql, val)
            conn.commit()
            myresult = cur.fetchone()
            if myresult is not None:
                if myresult != []:
                    result = myresult[0]
                    global fileDangTai
                    fileDangTai = upData(details, result, link1,fileDangTai)
                    
        with open('' + folder_path1 + '/TBMT_CDT.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CDT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.exceptions.ConnectionError as err :
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CDT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CDT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CDT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    return

def crawlDetail_FileDinhKemHSMT(data):
    nhapFile = []
    nhapFile.clear()
    for file in data:
        review_dic = json.loads(file['formValue'])
        datax = json.dumps(review_dic)
        if datax.find('sharedFiles') != -1:
            sharedFiles = review_dic['sharedFiles']
            if sharedFiles is not None:
                if sharedFiles != []:
                    for file_id in sharedFiles:
                        nhapFile.append([file_id,file['formCode'],file['chapterCode']])
        
    return nhapFile
                    

def crawlDetail_FileDinhKemHSMT(data):
    nhapFile = []
    nhapFile.clear()
    for file in data:
        review_dic = json.loads(file['formValue'])
        datax = json.dumps(review_dic)
        if datax.find('sharedFiles') != -1:
            sharedFiles = review_dic['sharedFiles']
            if sharedFiles is not None:
                if sharedFiles != []:
                    for file_id in sharedFiles:
                        nhapFile.append([file_id, file['formCode'], file['chapterCode']])

    return nhapFile


def crawlDetail_HangHoa(data):
    list_HH = []
    list_HH.clear()
    check_list = None
    if data is not None:
        if data['bidoInvBiddingDTO'] is not None:
            review = data['bidoInvBiddingDTO']
            for review1 in review:
                if review1['formValue'][:8] == '{"shared':
                    review_dic = json.loads(review1['formValue'])
                    table = review_dic['Table']
                    for hh in table:
                        data_hh = json.dumps(hh)
                        if data_hh.find('name') != -1:
                            check_list = 0
                            name = hh['name']
                            uom = hh['uom']
                            qty = hh['qty']
                            fromDate = hh['fromDate']
                            toDate = hh['toDate']
                            description = hh['description']
                            list_HH.append([name, uom, qty, fromDate, toDate, description])
                        else:
                            check_list = 1
                            name = hh['lotName']
                            LEPrice = hh['lotEstimatePrice']
                            cperiod = str(hh['cperiod']) + hh['cperiodUnit']
                            LPrice = hh['lotPrice']
                            if hh['lotGuaranteeValue'] == None:
                                LGValue = 0
                            else:
                                LGValue = hh['lotGuaranteeValue']
                            uom = hh['uom']
                            qty = hh['quantity']
                            list_HH.append([name, LEPrice, cperiod, LPrice, LGValue, uom, qty])

    return list_HH, check_list

def crawlDetail_HangHoa_CNTTT(data):
    a = []
    if data['bideContractorInputResultDTO'] is not None:
        if data['bideContractorInputResultDTO']['lotResultDTO'] is not None:
            if data['bideContractorInputResultDTO']['lotResultDTO'][0]['goodsList'] is not None:
                data_list = data['bideContractorInputResultDTO']['lotResultDTO'][0]['goodsList']
                reviews = json.loads(data_list)
                for review in reviews:
                    print(review['formValue']['lotContent']['Table'])
                    return review['formValue']['lotContent']['Table']
    return a

def CrawlDetail_TT_DA(code, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'JSESSIONID': 'kxcFyFjRtLzqDFb362ipIUfUbMaNTQ4mQDv-CNf8.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1677139841143',
        '_ga_19996Z37EE': 'GS1.1.1677139121.29.1.1677139862.0.0.0',
        'citrix_ns_id': 'AAE7sRz3YzurjrQAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==JiP3Yw==wr5VWU6vNJBiNwdpdC2k2ut_LOo=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; JSESSIONID=kxcFyFjRtLzqDFb362ipIUfUbMaNTQ4mQDv-CNf8.dc_app1_02; LFR_SESSION_STATE_20103=1677139841143; _ga_19996Z37EE=GS1.1.1677139121.29.1.1677139862.0.0.0; citrix_ns_id=AAE7sRz3YzurjrQAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==JiP3Yw==wr5VWU6vNJBiNwdpdC2k2ut_LOo=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-bidp-project-p&stepCode=project-step-1&id=7bd3d764-dd88-4200-8190-029e953dda38&notifyId=undefined&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=undefined&bidMode=undefined&notifyNo=undefined&planNo=undefined&pno=PR2300006909',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bidp-project-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
            
        )

        json_data = response.json()
        if json_data is None:
            return
        if json_data['linkedPublishPlan'] is None:
            return
        else:
            reviews = json_data['linkedPublishPlan']

        if json_data['projectDTO'] is None:
            return
        else:
            reviews1 = json_data['projectDTO']

        if reviews1['no'] is None:
            reviews1['no'] = 0

        if reviews1['status'] is None:
            reviews1['status'] = 0

        if reviews1['name'] is None:
            reviews1['name'] = 0

        if reviews1['investTarget'] is None:
            reviews1['investTarget'] = 0

        if reviews1['investorName'] is None:
            reviews1['investorName'] = 0

        if json_data['competentPersons'] is None:
            json_data['competentPersons'] = 0

        if reviews1['period'] is None:
            reviews1['period'] = ''
        else:
            if reviews1['periodUnit'] is None:
                reviews1['periodUnit'] = ''
            else:
                if reviews1['periodUnit'] == '1':
                    reviews1['periodUnit'] = 'Năm'
                elif reviews1['periodUnit'] == '2':
                    reviews1['periodUnit'] = 'Tháng'
                elif reviews1['periodUnit'] == '3':
                    reviews1['periodUnit'] = 'Ngày'

        thoigian = str(reviews1['period']) + str(reviews1['periodUnit'])

        if json_data['pgroup'] is None:
            json_data['pgroup'] = 0

        if json_data['pform'] is None:
            json_data['pform'] = 0

        if json_data['isOda'] is None:
            json_data['isOda'] = 0
        else:
            if json_data['isOda'] == False:
                json_data['isOda'] = 'Không'
            elif json_data['isOda'] == True:
                json_data['isOda'] = 'Có'

        if json_data['districtName'] is None:
            json_data['districtName'] = ''

        if json_data['provName'] is None:
            json_data['provName'] = ''

        diadiem = str(json_data['districtName']) + str(json_data['provName'])

        if json_data['investTotal'] is None:
            json_data['investTotal'] = 0
            if reviews1['investTotal'] is None:
                reviews1['investTotal'] = 0
            else:
                tongmucdautu = reviews1['investTotal']
        else:
            tongmucdautu = json_data['investTotal']

        if json_data['decisionNo'] is None:
            json_data['decisionNo'] = 0

        if json_data['decisionDate'] is None:
            json_data['decisionDate'] = 0

        if json_data['decisionAgency'] is None:
            json_data['decisionAgency'] = 0

        if json_data['decisionFileId'] is None:
            json_data['decisionFileId'] = 0
        else:
            link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + str(json_data['decisionFileId'])
        nhap = [0]
        nhap.clear()
        for review in reviews:
            if review['planNo'] is None:
                review['planNo'] = 0

            if review['name'] is None:
                review['name'] = 0

            if review['investTotal'] is None:
                review['investTotal'] = 0

            nhap.append([review['planNo'], review['name'], review['investTotal']])

        details.extend(
            [reviews1['no'], reviews1['status'], reviews1['name'], reviews1['investTarget'], reviews1['investorName'],
             json_data['competentPersons'], thoigian, json_data['pgroup'], json_data['pform'], json_data['isOda'],
             diadiem, tongmucdautu, json_data['decisionNo'], json_data['decisionDate'], json_data['decisionAgency'],
             link1, nhap])

        with open('' + folder_path1 + '/DA.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()



    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so du an bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.exceptions.ConnectionError as err :
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so du an bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()

        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so du an bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so du an bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    return


def SoTrangTinTucDongThau(startDay, endDay):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'A01pYkikrvtLTLatxAdtESmHJgoG0zZIAQNfwZHD.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1677148752780',
        '_ga_19996Z37EE': 'GS1.1.1677147004.31.1.1677148835.0.0.0',
        'citrix_ns_id': 'AAU7lEH3YzvqWrYAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==KEb3Yw==lvHrw4InkjwfEla_RzCLvQhuRbc=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=A01pYkikrvtLTLatxAdtESmHJgoG0zZIAQNfwZHD.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677148752780; _ga_19996Z37EE=GS1.1.1677147004.31.1.1677148835.0.0.0; citrix_ns_id=AAU7lEH3YzvqWrYAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==KEb3Yw==lvHrw4InkjwfEla_RzCLvQhuRbc=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        data = '{"pageSize":8,"pageNumber":"0","query":[{"index":"es-contractor-selection","keyWord":"","matchType":"all","matchFields":["notifyNo","bidName"],"filters":[{"fieldName":"bidCloseDate","searchType":"range","from":"' + startDay + 'T00:00:00.000Z","to":"' + endDay + 'T23:59:59.059Z"},{"fieldName":"type","searchType":"in","fieldValues":["es-notify-contractor"]}]}]}'
        response = requests.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/smart/search',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
        )
        json_data = response.json()
        reviews = json_data
        totalPageNumber = reviews['page']['totalPages']

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc dong thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc dong thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc dong thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path + "/log.txt", "a")
        f.write("Khong lay duoc so trang tin tuc dong thau")
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    return totalPageNumber


def CrawlMaTinTucDongThau(pageNumber, codes, details, session1, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'A01pYkikrvtLTLatxAdtESmHJgoG0zZIAQNfwZHD.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1677148752780',
        '_ga_19996Z37EE': 'GS1.1.1677147004.31.1.1677148835.0.0.0',
        'citrix_ns_id': 'AAU7lEH3YzvqWrYAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==KEb3Yw==lvHrw4InkjwfEla_RzCLvQhuRbc=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=A01pYkikrvtLTLatxAdtESmHJgoG0zZIAQNfwZHD.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677148752780; _ga_19996Z37EE=GS1.1.1677147004.31.1.1677148835.0.0.0; citrix_ns_id=AAU7lEH3YzvqWrYAAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==KEb3Yw==lvHrw4InkjwfEla_RzCLvQhuRbc=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=index',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        data = '{"pageSize":8,"pageNumber":"' + str(
            pageNumber) + '","query":[{"index":"es-contractor-selection","keyWord":"","matchType":"all","matchFields":["notifyNo","bidName"],"filters":[{"fieldName":"bidCloseDate","searchType":"range","from":"' + startDay + 'T00:00:00.000Z","to":"' + endDay + 'T23:59:59.059Z"},{"fieldName":"type","searchType":"in","fieldValues":["es-notify-contractor"]}]}]}'
        response = requests.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/smart/search',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
        )
        json_data = response.json()
        data = json.dumps(json_data)
        reviews = json_data['page']['content']

        for review in reviews:
            if review['id'] is None:
                review['id'] = 0

            if review['notifyNo'] is None:
                review['notifyNo'] = 0

            if review['type'] is None:
                review['type'] = 0

            if review['stepCode'] is None:
                review['stepCode'] = 0

            if review['isInternet'] is None:
                review['isInternet'] = ''

            if review['statusForNotify'] is None:
                review['statusForNotify'] = 0
            else:
                inputResultId = ''
                if review['statusForNotify'] == 'CNTTT':
                    if review['inputResultId'] is None:
                        inputResultId = ''
                    else:
                        inputResultId = review['inputResultId']
            review_data = json.dumps(review)
            bidField = ''

            if review_data.find('bidField') != -1 :
                if review['bidField'] is None:
                    review['bidField'] = ''
                    bidField = ''
                else:
                    bidField = review['bidField']
            else:
                bidField = ''

            if review['notifyVersion'] is None:
                review['notifyVersion'] = ''

            if review['notifyVersion'] is None:
                review['notifyVersion'] = ''

            codes.append([review['id'],#0
                          review['notifyNo'],#1
                          
                          review['type'],#2
                          
                          review['stepCode'],#3
                          
                          review['statusForNotify'],#4
                          
                          inputResultId,#5
                          
                          review['isInternet'],#6
                          bidField,#7
                          review['notifyVersion']])

        for code in codes:
            if code[4] == 'CNTTT':
                if code[6] == 1:
                    CrawlDetail_DT_CNTTT(code=code[0], details=details, session1=session1, codes=code,
                                         folder_path1=folder_path1, code1=code[1], code2=code[5])

                if code[6] == 0:
                    CrawDetail_DT_CNTTT_KQM(inputResultId=code[5], details=details, session1=session1, codes=code,
                                            folder_path1=folder_path1)

            #if code[4] == 'DHT':
                #CrawlDetail_DT_DHT(code=code[0],details=details,session1=session1,codes=code,folder_path1=folder_path1)

            #if code[4] == 'KCNTTT':
                #if code[6] == 1:
                    #CrawlDetail_DT_KCNTTT(code=code[0],details=details,session1=session1,codes=code,folder_path1=folder_path1)
                #elif code[6] == 0:
                    #CrawDetail_DT_KCNTTT_KQM(inputResultId=code[5],details=details,session1=session1,codes=code,folder_path1=folder_path1)

            if code[4] == 'DXT':
                if code[6] == 1:
                    if code[7] == 'TV':
                        if code[3] == 'notify-contractor-step-2-kqmt':
                            CrawlDetail_DT_DXT_TV_KQMT(code=code[0],details=details,session1=session1,codes=code,folder_path1=folder_path1,notify_no=code[1],mode='kqmt')
                            #Code DXT KQMT
                        elif code[3] == 'notify-contractor-step-3-dsntdkt':
                            CrawlDetail_DT_DXT_TV_DSNTDKT(code=code[0],details=details,session1=session1,codes=code,folder_path1=folder_path1,notify_no=code[1],mode = 'dsntdkt')
                            #Code DXT DSNTDXKT
                        else:
                            print(code)
                            #Tim con code nao khac khong
                    else:
                        news_id = CrawlDetail_DT_DXT(code=code[0],details=details,session1=session1,codes=code,folder_path1=folder_path1,notify_no=code[1],mode='else')

        codes.clear()

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc dong thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc dong thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc dong thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        k = int(pageNumber) + 1
        h = "{}".format(k)
        f.write("Trang bi loi khong lay duoc du lieu tin tuc dong thau: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        codes.clear()
        details.clear()
        pass

    return


def CrawlDetail_DT_DXT(code, details, session1, codes, folder_path1, notify_no,mode):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'LFR_SESSION_STATE_20103': '1677207191833',
        'JSESSIONID': 'rKdcx8DYHay2zkRr5ndZqzXZ6jN5HI0muLhOk7QL.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1677204596.32.1.1677207694.0.0.0',
        'citrix_ns_id': 'AAE7chz4Yzs0w7YAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==FSz4Yw==v1HcXeWvpdwRKX52o0Vz9AiBsLA=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1677207191833; JSESSIONID=rKdcx8DYHay2zkRr5ndZqzXZ6jN5HI0muLhOk7QL.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1677204596.32.1.1677207694.0.0.0; citrix_ns_id=AAE7chz4Yzs0w7YAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==FSz4Yw==v1HcXeWvpdwRKX52o0Vz9AiBsLA=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=74daf170-49dc-40f6-b1d4-aa6ea598e52c&notifyId=74daf170-49dc-40f6-b1d4-aa6ea598e52c&inputResultId=undefined&bidOpenId=eec02f9e-d571-4acb-83c3-17e5918bc88e&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300020092&planNo=PL2300014512&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    cookies2 = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        '5321a273c51a75133e0fb1cd75e32e27': 'c47b17d3ecf7b555d4037c14903e3631',
        'JSESSIONID': 'Tj83BjZs1M_f9_pbniA_9inYOFGsr9vcSwdR-4c_.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1680148675471',
        '_ga_19996Z37EE': 'GS1.1.1680142938.44.1.1680148687.0.0.0',
        'citrix_ns_id': 'AAE7rgglZDteF-kAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==WwwlZA==YlgzyAh0PhUTuzLIkgwZvibVzKs=',
    }

    headers2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; 5321a273c51a75133e0fb1cd75e32e27=c47b17d3ecf7b555d4037c14903e3631; JSESSIONID=Tj83BjZs1M_f9_pbniA_9inYOFGsr9vcSwdR-4c_.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1680148675471; _ga_19996Z37EE=GS1.1.1680142938.44.1.1680148687.0.0.0; citrix_ns_id=AAE7rgglZDteF-kAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==WwwlZA==YlgzyAh0PhUTuzLIkgwZvibVzKs=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=c8229d00-e936-4353-ae34-a4c032849fac&notifyId=c8229d00-e936-4353-ae34-a4c032849fac&inputResultId=undefined&bidOpenId=273cd794-267e-4eb0-b570-f2f83b74d20f&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_HTHS&notifyNo=IB2300040650&planNo=PL2300021810&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera GX";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bido-notify-contractor-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data = response.json()
        i = random.randrange(1,10)
        time.sleep(i)
        data2 = '{"notifyNo":"' + codes[1] + '","type":"TBMT","packType":0}'
        response2 = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/ldtkqmt/bid-notification-p/get-by-id',
            cookies=cookies2,
            headers=headers2,
            data=data2,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data2 = response2.json()
        review2 = json_data2
        i = random.randrange(1,10)
        time.sleep(i)
        data3 = '{"id":"' + code + '"}'
        response3 = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-notify-contractor-out/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data3 = response3.json()

        nhap1 = [0]
        nhap1.clear()
        dem = 0
        dem1 = 0
        datesucces = ""

        if review2 is not None:
            if review2['bidoBidroundMngViewDTO'] is not None:
                if review2['bidoBidroundMngViewDTO']["successBidOpenDate"] is not None:
                    datesucces = review2['bidoBidroundMngViewDTO']["successBidOpenDate"]

            if review2['bidSubmissionByContractorViewResponse'] is None:
                nhap1, dem1, datesucces = CrawlDetail_DT_DXT_2(code=code, session1=session1, codes=codes, folder_path1=folder_path1, notify_no=notify_no)

            else:
                if review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is not None:
                    for nhathau in review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
                        if nhathau['contractorCode'] is None:
                            nhathau['contractorCode'] = ''

                        if nhathau['contractorName'] is None:
                            nhathau['contractorName'] = ''

                        if nhathau['bidPrice'] is None:
                            nhathau['bidPrice'] = ''

                        if nhathau['alternativeTech'] is None:
                            nhathau['alternativeTech'] = ''

                        if nhathau['bidFinalPrice'] is None:
                            nhathau['bidFinalPrice'] = ''

                        if nhathau['bidValidityNum'] is None:
                            nhathau['bidValidityNum'] = ''

                        if nhathau['bidGuarantee'] is None:
                            nhathau['bidGuarantee'] = ''

                        if nhathau['bidGuaranteeValidity'] is None:
                            nhathau['bidGuaranteeValidity'] = ''

                        if nhathau['contractPeriodDT'] is None:
                            nhathau['contractPeriodDT'] = ''

                        if nhathau['contractPeriodDTUnit'] is None:
                            nhathau['contractPeriodDTUnit'] = ''

                        nhap1.append([nhathau['contractorCode'],
                                      nhathau['contractorName'],
                                      nhathau['bidPrice'],
                                      nhathau['alternativeTech'],
                                      nhathau['bidFinalPrice'],
                                      nhathau['bidValidityNum'],
                                      nhathau['bidGuarantee'],
                                      nhathau['bidGuaranteeValidity'],
                                      str(nhathau['contractPeriodDT']) + nhathau['contractPeriodDTUnit']])
                        dem = dem + 1

        if dem < dem1:
            dem = dem1

        review = 0
        data = json.dumps(json_data)
        check = 0

        if json_data is not None:
            data = json.dumps(json_data)
            if data.find('bidoNotifyContractorP') != -1:
                if json_data['bidoNotifyContractorP'] is not None:
                    review = json_data['bidoNotifyContractorP']
                    if review['cPeriod'] is None:
                        review['cPeriod'] = 0
                    if review['cPeriodUnit'] is None:
                        review['cPeriodUnit'] = 0
                    a = str(review['cPeriod']) + str(review['cPeriodUnit'])
                    if review['cType'] is not None:
                        v = review['cType']
                    else:
                        v = 0
                else:
                    check = 1

            elif data.find('bidoNotifyContractorM') != -1:
                if json_data['bidoNotifyContractorM'] is not None:
                    review = json_data['bidoNotifyContractorM']
                    if review['contractPeriod'] is None:
                        review['contractPeriod'] = 0
                    if review['contractPeriodUnit'] is None:
                        review['contractPeriodUnit'] = 0
                    a = str(review['contractPeriod']) + str(review['contractPeriodUnit'])
                    if review['contractType'] is not None:
                        v = review['contractType']
                    else:
                        v = 0
                else:
                    check = 1

        if check == 1:
            json_data = json_data3
            if json_data is not None:
                data = json.dumps(json_data)
                if data.find('bidoNotifyContractorP') != -1:
                    if json_data['bidoNotifyContractorP'] is not None:
                        review = json_data['bidoNotifyContractorP']
                        if review['cPeriod'] is None:
                            review['cPeriod'] = 0
                        if review['cPeriodUnit'] is None:
                            review['cPeriodUnit'] = 0
                        a = str(review['cPeriod']) + str(review['cPeriodUnit'])
                        if review['cType'] is not None:
                            v = review['cType']
                        else:
                            v = 0
                    else:
                        check = 1

                elif data.find('bidoNotifyContractorM') != -1:
                    if json_data['bidoNotifyContractorM'] is not None:
                        review = json_data['bidoNotifyContractorM']
                        if review['contractPeriod'] is None:
                            review['contractPeriod'] = 0
                        if review['contractPeriodUnit'] is None:
                            review['contractPeriodUnit'] = 0
                        a = str(review['contractPeriod']) + str(review['contractPeriodUnit'])
                        if review['contractType'] is not None:
                            v = review['contractType']
                        else:
                            v = 0
                    else:
                        check = 1

        fee = 0
        if review['bidForm'] is None:
            review['bidForm'] = ''
        else:
            if review['bidForm'] == 'CHCT':
                review['bidForm'] = 'Chào hàng cạnh tranh'
            if review['bidForm'] == 'DTRR':
                review['bidForm'] = 'Đấu thầu rộng rãi'
            if review['bidForm'] == 'CHCTRG':
                review['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
            if review['bidForm'] == 'CDTRG':
                review['bidForm'] = 'Chỉ định thầu rút gọn'

        if review['isInternet'] is None:
            review['isInternet'] = ''
        if review['isInternet'] == 1:
            if review['bidForm'] == 'Đấu thầu rộng rãi' or review['bidForm'] == 'DTHC' or review['bidForm'] == 'MSTT':
                fee = '330,000 VND'
            elif review['bidForm'] == 'Chào hàng cạnh tranh' or review['bidForm'] == 'Chào hàng cạnh tranh rút gọn':
                fee = '220,000 VND'
        elif review['isInternet'] == 0:
            if review['feeValue'] is None:
                fee = ''
            else:
                fee = str(review['feeValue']) + 'VND'

        if review['notifyNo'] is None:
            review['notifyNo'] = ''

        if review['publicDate'] is None:
            review['publicDate'] = '0'

        if review['planNo'] is None:
            review['planNo'] = ''

        if review['planType'] is None:
            review['planType'] = ''
        else:
            if review['planType'] == 'DTPT':
                review['planType'] = 'Chi đầu tư phát triển'
            elif review['planType'] == 'TX':
                review['planType'] = 'Chi thường xuyên'

        if review['planName'] is None:
            review['planName'] = ''

        if review['bidName'] is None:
            review['bidName'] = ''

        if review['investorName'] is None:
            review['investorName'] = ''

        if review['procuringEntityName'] is None:
            review['procuringEntityName'] = ''

        if review['capitalDetail'] is None:
            review['capitalDetail'] = ''

        if review['investField'] is None:
            review['investField'] = ''

        if review['bidForm'] is None:
            review['bidForm'] = ''
        else:
            if review['bidForm'] == 'CHCT':
                review['bidForm'] = 'Chào hàng cạnh tranh'
            if review['bidForm'] == 'DTRR':
                review['bidForm'] = 'Đấu thầu rộng rãi'
            if review['bidForm'] == 'CHCTRG':
                review['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
            if review['bidForm'] == 'CDTRG':
                review['bidForm'] = 'Chỉ định thầu rút gọn'

        if review['isDomestic'] is None:
            review['isDomestic'] = ''
        else:
            if review['isDomestic'] == 1:
                review['isDomestic'] = 'Trong nước'
            elif review['isDomestic'] == 0:
                review['isDomestic'] = 'Quốc tế'

        if review['bidMode'] is None:
            review['bidMode'] = ''
        else:
            if review['bidMode'] == '1_MTHS':
                review['bidMode'] = 'Một giai đoạn một túi hồ sơ'
            elif review['bidMode'] == '1_HTHS':
                review['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

        if review['isInternet'] is None:
            review['isInternet'] = ''
        else:
            if review['isInternet'] == 1:
                review['isInternet'] = 'Qua mạng'
            elif review['isInternet'] == 0:
                review['isInternet'] = 'Không qua mạng'

        if review['issueLocation'] is None:
            review['issueLocation'] = ''

        if review['receiveLocation'] is None:
            review['receiveLocation'] = ''

        if review['bidCloseDate'] is None:
            review['bidCloseDate'] = ''

        if review['bidOpenDate'] is None:
            review['bidOpenDate'] = ''

        if review['bidOpenLocation'] is None:
            review['bidOpenLocation'] = ''

        if review['bidValidityPeriod'] is None:
            review['bidValidityPeriod'] = ''

        if review['bidValidityPeriodUnit'] is None:
            review['bidValidityPeriodUnit'] = ''
        x = str(review['bidValidityPeriod']) + ' ' + str(review['bidValidityPeriodUnit'])

        if json_data['bidInvContractorOfflineDTO'] is not None:
            if json_data['bidInvContractorOfflineDTO']['decisionNo'] is None:
                decisionNo = ''
            else:
                decisionNo = json_data['bidInvContractorOfflineDTO']['decisionNo']

            if json_data['bidInvContractorOfflineDTO']['decisionDate'] is None:
                decisionDate = ''
            else:
                decisionDate = json_data['bidInvContractorOfflineDTO']['decisionDate']

            if json_data['bidInvContractorOfflineDTO']['decisionAgency'] is None:
                decisionAgency = ''
            else:
                decisionAgency = json_data['bidInvContractorOfflineDTO']['decisionAgency']

            if json_data['bidInvContractorOfflineDTO']['decisionFileId'] is None:
                decisionFileId = ''
                link1 = ''
            else:
                decisionFileId = json_data['bidInvContractorOfflineDTO']['decisionFileId']
                link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + decisionFileId
        else:
            decisionNo = ''
            decisionDate = ''
            decisionAgency = ''
            decisionFileId = ''
            link1 = ''

        if review['id'] is None:
            review['id'] = ''
            link2 = ''
        else:
            link2 = 'https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=' + review['id']

        if review['bidPrice'] is None:
            review['bidPrice'] = ''
        if review2['bidoBidroundMngViewDTO'] is not None:
            if review2['bidoBidroundMngViewDTO']['successBidOpenDate'] is None:
                bien = ''
            else:
                bien = review2['bidoBidroundMngViewDTO']['successBidOpenDate']
            if review2['bidoBidroundMngViewDTO']['countContractor'] is not None:
                count = review2['bidoBidroundMngViewDTO']['countContractor']
        else:
            bien = ''

        if review['investField'] == "HH":
            review['investField'] = "Hàng hóa"
        elif review['investField'] == "PTV":
            review['investField'] = "Phi tư vấn"
        elif review['investField'] == "TV":
            review['investField'] = "Tư vấn"
        elif review['investField'] == "XL":
            review['investField'] = "Xây lắp"

        details.extend([
            review['notifyNo'],#0
            review['publicDate'],#1
            review["notifyVersion"],#2
            review['planNo'],#3
            review['planType'],#4
            review['planName'],#5
            review['bidName'],#6
            review['investorName'],#7
            review['procuringEntityName'],#8
            review['capitalDetail'],#9
            review['investField'],#10
            review['bidForm'],#11
            v,#12
            review['isDomestic'],#13
            review['bidMode'],#14
            a,#15
            review['isInternet'],#16
            review['issueLocation'],#17
            fee,#18
            review['receiveLocation'],#19
            b,#20
            review['bidCloseDate'],#21
            review['bidOpenDate'],#22
            review['bidOpenLocation'],#23
            str(review['bidValidityPeriod']) + str(review['bidValidityPeriodUnit']),#24
            decisionNo,#25
            decisionDate,#26
            decisionAgency,#27
            link1,#28
            link2,#29
            review['bidPrice'],#30
            dem,#31
            bien,#32
            nhap1,#33
            datesucces,#34
            ])
        
        bidType = upABN_db.bid_type(review['investField'])
        bidMethod = upABN_db.bid_method(review['isInternet'])
        crea_at = upABN_db.timeUpd()
        tim_open = upABN_db.time_close(review['bidOpenDate'])

        with open('' + folder_path1 + '/DXT.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        if upABN_db.ktTrungDL(review['notifyNo'], review["notifyVersion"]) == None:

            if details[10] == 'Tư vấn' or details[10] == 'TV':

                if mode == 'dsntdkt':
                    news_id = upABN_db.upDataDB_1_DXT_TV(7, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'], review["notifyVersion"])
                    open_result_status = 'complete_gd_hskt'
                    upABN_db.upDataDB_DXT_TV(tim_open, news_id,open_result_status)

                elif mode =='kqmt':
                    news_id = upABN_db.upDataDB_1_DXT_TV(7, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'], review["notifyVersion"])
                    open_result_status = 'open_hskt_complete'
                    upABN_db.upDataDB_DXT_TV(tim_open, news_id,open_result_status)
                    upABNDetail_db.upData_DXT_TV(details, news_id)
                    upABO_db.upDataDB_TV(details, news_id)

            else:
                news_id = upABN_db.upDataDB_1_DXT(7, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'], review["notifyVersion"])
                
                upABN_db.upDataDB_DXT(tim_open, news_id)

                upABNDetail_db.upData_DXT(details, news_id)

                upABO_db.upDataDB(details, news_id)
        details.clear()
        return news_id


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass
    return 'false'


def CrawlDetail_DT_DXT_2(code, session1, codes, folder_path1, notify_no):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        '5321a273c51a75133e0fb1cd75e32e27': '90d57e96398dec0a2d505d16e8dab718',
        'JSESSIONID': 'j42sgmGH7hD0CrMTwBqHFE7zrzf6v-YAYv0pq7r4.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1678953886960',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1678952934.12.1.1678954032.0.0.0',
        'citrix_ns_id': 'AAY76skSZDvmstQAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==vdESZA==FJrG_ayohQqdZRWrr4alrzqYQOU=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; 5321a273c51a75133e0fb1cd75e32e27=90d57e96398dec0a2d505d16e8dab718; JSESSIONID=j42sgmGH7hD0CrMTwBqHFE7zrzf6v-YAYv0pq7r4.dc_app1_02; LFR_SESSION_STATE_20103=1678953886960; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1678952934.12.1.1678954032.0.0.0; citrix_ns_id=AAY76skSZDvmstQAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==vdESZA==FJrG_ayohQqdZRWrr4alrzqYQOU=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=9506398d-3028-4735-9d7b-6a9b41f9540b&notifyId=9506398d-3028-4735-9d7b-6a9b41f9540b&inputResultId=undefined&bidOpenId=6207a849-263c-421d-a328-15cd627578d5&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=KHAC&bidMode=1_MTHS&notifyNo=IB2300037374&planNo=PL2300024675&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera GX";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/kqmt/bid-notify-contractor-out/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data = response.json()
        review = json_data
        nhap1 = []
        nhap1.clear()
        dem = 0
        data_dump = json.dumps(json_data)
        datesucces = ''
        if review is not None:
            if data_dump.find('bidoBidroundMngViewDTO') != -1:
                if review['bidoBidroundMngViewDTO'] is not None:
                    if review['bidoBidroundMngViewDTO']["successBidOpenDate"] is not None:
                        datesucces = review['bidoBidroundMngViewDTO']["successBidOpenDate"]

            if review['bidSubmissionByContractorViewResponse'] is not None:
                if review['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is not None:
                    for nhathau in review['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
                        if nhathau['contractorCode'] is None:
                            nhathau['contractorCode'] = ''

                        if nhathau['contractorName'] is None:
                            nhathau['contractorName'] = ''

                        if nhathau['bidPrice'] is None:
                            nhathau['bidPrice'] = ''

                        if nhathau['alternativeTech'] is None:
                            nhathau['alternativeTech'] = ''

                        if nhathau['bidFinalPrice'] is None:
                            nhathau['bidFinalPrice'] = ''

                        if nhathau['bidValidityNum'] is None:
                            nhathau['bidValidityNum'] = ''

                        if nhathau['bidGuarantee'] is None:
                            nhathau['bidGuarantee'] = ''

                        if nhathau['bidGuaranteeValidity'] is None:
                            nhathau['bidGuaranteeValidity'] = ''

                        if nhathau['contractPeriodDT'] is None:
                            nhathau['contractPeriodDT'] = ''

                        if nhathau['contractPeriodDTUnit'] is None:
                            nhathau['contractPeriodDTUnit'] = ''
                
                        nhap1.append([nhathau['contractorCode'],#0
                                      nhathau['contractorName'],#1
                                      nhathau['bidPrice'],#2
                                      nhathau['alternativeTech'],#3
                                      nhathau['bidFinalPrice'],#4
                                      nhathau['bidValidityNum'],#5
                                      nhathau['bidGuarantee'],#6
                                      nhathau['bidGuaranteeValidity'],#7
                                      str(nhathau['contractPeriodDT']) + nhathau['contractPeriodDTUnit']#8
                                      ])
                        dem = dem + 1

        return nhap1, dem, datesucces

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass
    return

def CrawlDetail_DT_DXT_TV_KQMT(code,details,session1,codes,folder_path1,notify_no,mode):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'LFR_SESSION_STATE_20103': '1677207191833',
        'JSESSIONID': 'rKdcx8DYHay2zkRr5ndZqzXZ6jN5HI0muLhOk7QL.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1677204596.32.1.1677207694.0.0.0',
        'citrix_ns_id': 'AAE7chz4Yzs0w7YAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==FSz4Yw==v1HcXeWvpdwRKX52o0Vz9AiBsLA=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1677207191833; JSESSIONID=rKdcx8DYHay2zkRr5ndZqzXZ6jN5HI0muLhOk7QL.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1677204596.32.1.1677207694.0.0.0; citrix_ns_id=AAE7chz4Yzs0w7YAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==FSz4Yw==v1HcXeWvpdwRKX52o0Vz9AiBsLA=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=74daf170-49dc-40f6-b1d4-aa6ea598e52c&notifyId=74daf170-49dc-40f6-b1d4-aa6ea598e52c&inputResultId=undefined&bidOpenId=eec02f9e-d571-4acb-83c3-17e5918bc88e&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300020092&planNo=PL2300014512&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    cookies2 = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '_ga_19996Z37EE': 'deleted',
        '5321a273c51a75133e0fb1cd75e32e27': 'c47b17d3ecf7b555d4037c14903e3631',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': '2rSBAJO2OrQqJqPQwr7KLbpm09apgRvh-CVhJEEC.dc_app1_02',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1680168644771',
        '_ga_19996Z37EE': 'GS1.1.1680167073.48.1.1680168732.0.0.0',
        'citrix_ns_id': 'AAM7vFYlZDssIOoAAAAAADuFeyfrzB16Q6f2O3wkwp-X_KBiAk_jQriThj-xlt31Ow==qFolZA==JH3rVDxhrSsoSJWPQ6uj5VC23jQ=',
    }

    headers2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; _ga_19996Z37EE=deleted; 5321a273c51a75133e0fb1cd75e32e27=c47b17d3ecf7b555d4037c14903e3631; _ga_19996Z37EE=deleted; JSESSIONID=2rSBAJO2OrQqJqPQwr7KLbpm09apgRvh-CVhJEEC.dc_app1_02; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1680168644771; _ga_19996Z37EE=GS1.1.1680167073.48.1.1680168732.0.0.0; citrix_ns_id=AAM7vFYlZDssIOoAAAAAADuFeyfrzB16Q6f2O3wkwp-X_KBiAk_jQriThj-xlt31Ow==qFolZA==JH3rVDxhrSsoSJWPQ6uj5VC23jQ=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=719b5e6c-0692-4eb9-a36a-aa8a58dba5c9&notifyId=719b5e6c-0692-4eb9-a36a-aa8a58dba5c9&inputResultId=undefined&bidOpenId=dc3a3618-9a92-4b6c-bd57-f45ac6b8ce79&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_HTHS&notifyNo=IB2300033071&planNo=PL2300023643&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera GX";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bido-notify-contractor-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data = response.json()
        i = random.randrange(1,10)
        time.sleep(i)
        data2 = '{"notifyNo":"' + codes[1] + '","type":"TBMT","packType":1}'
        response2 = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/ldtkqmt/bid-notification-p/get-by-id',
            cookies=cookies2,
            headers=headers2,
            data=data2,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data2 = response2.json()
        review2 = json_data2

        i = random.randrange(1,10)
        time.sleep(i)
        data3 = '{"id":"' + code + '"}'
        response3 = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-notify-contractor-out/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data3 = response3.json()

        nhap1 = [0]
        nhap1.clear()
        dem = 0
        dem1 = 0
        datesucces = ""

        if review2 is not None:
            if review2['bidoBidroundMngViewDTO'] is not None:
                if review2['bidoBidroundMngViewDTO']["successBidOpenDate"] is not None:
                    datesucces = review2['bidoBidroundMngViewDTO']["successBidOpenDate"]

            if review2['bidSubmissionByContractorViewResponse'] is None:
                nhap1, dem1, datesucces = CrawlDetail_DT_DXT_TV_2(code=code, session1=session1, codes=codes,folder_path1=folder_path1, notify_no=notify_no)

            else:
                if review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is not None:
                    for nhathau in review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
                        if nhathau['contractorCode'] is None:
                            nhathau['contractorCode'] = ''

                        if nhathau['contractorName'] is None:
                            nhathau['contractorName'] = ''

                        if nhathau['bidPrice'] is None:
                            nhathau['bidPrice'] = ''

                        if nhathau['alternativeTech'] is None:
                            nhathau['alternativeTech'] = ''

                        if nhathau['bidFinalPrice'] is None:
                            nhathau['bidFinalPrice'] = ''

                        if nhathau['bidValidityNum'] is None:
                            nhathau['bidValidityNum'] = ''

                        if nhathau['bidGuarantee'] is None:
                            nhathau['bidGuarantee'] = ''

                        if nhathau['bidGuaranteeValidity'] is None:
                            nhathau['bidGuaranteeValidity'] = ''

                        if nhathau['contractPeriodDT'] is None:
                            nhathau['contractPeriodDT'] = ''

                        if nhathau['contractPeriodDTUnit'] is None:
                            nhathau['contractPeriodDTUnit'] = ''

                        nhap1.append([nhathau['contractorCode'],
                                      nhathau['contractorName'],
                                      nhathau['bidPrice'],
                                      nhathau['alternativeTech'],
                                      nhathau['bidFinalPrice'],
                                      nhathau['bidValidityNum'],
                                      nhathau['bidGuarantee'],
                                      nhathau['bidGuaranteeValidity'],
                                      str(nhathau['contractPeriodDT']) + nhathau['contractPeriodDTUnit']])
                        dem = dem + 1

        if dem < dem1:
            dem = dem1

        review = 0
        data = json.dumps(json_data)
        check = 0

        if json_data is not None:
            data = json.dumps(json_data)
            if data.find('bidoNotifyContractorP') != -1:
                if json_data['bidoNotifyContractorP'] is not None:
                    review = json_data['bidoNotifyContractorP']
                    if review['cPeriod'] is None:
                        review['cPeriod'] = 0
                    if review['cPeriodUnit'] is None:
                        review['cPeriodUnit'] = 0
                    a = str(review['cPeriod']) + str(review['cPeriodUnit'])
                    if review['cType'] is not None:
                        v = review['cType']
                    else:
                        v = 0
                else:
                    check = 1

            elif data.find('bidoNotifyContractorM') != -1:
                if json_data['bidoNotifyContractorM'] is not None:
                    review = json_data['bidoNotifyContractorM']
                    if review['contractPeriod'] is None:
                        review['contractPeriod'] = 0
                    if review['contractPeriodUnit'] is None:
                        review['contractPeriodUnit'] = 0
                    a = str(review['contractPeriod']) + str(review['contractPeriodUnit'])
                    if review['contractType'] is not None:
                        v = review['contractType']
                    else:
                        v = 0
                else:
                    check = 1

        if check == 1:
            json_data = json_data3
            if json_data is not None:
                data = json.dumps(json_data)
                if data.find('bidoNotifyContractorP') != -1:
                    if json_data['bidoNotifyContractorP'] is not None:
                        review = json_data['bidoNotifyContractorP']
                        if review['cPeriod'] is None:
                            review['cPeriod'] = 0
                        if review['cPeriodUnit'] is None:
                            review['cPeriodUnit'] = 0
                        a = str(review['cPeriod']) + str(review['cPeriodUnit'])
                        if review['cType'] is not None:
                            v = review['cType']
                        else:
                            v = 0
                    else:
                        check = 1

                elif data.find('bidoNotifyContractorM') != -1:
                    if json_data['bidoNotifyContractorM'] is not None:
                        review = json_data['bidoNotifyContractorM']
                        if review['contractPeriod'] is None:
                            review['contractPeriod'] = 0
                        if review['contractPeriodUnit'] is None:
                            review['contractPeriodUnit'] = 0
                        a = str(review['contractPeriod']) + str(review['contractPeriodUnit'])
                        if review['contractType'] is not None:
                            v = review['contractType']
                        else:
                            v = 0
                    else:
                        check = 1

        fee = 0
        if review['bidForm'] is None:
            review['bidForm'] = ''
        else:
            if review['bidForm'] == 'CHCT':
                review['bidForm'] = 'Chào hàng cạnh tranh'
            if review['bidForm'] == 'DTRR':
                review['bidForm'] = 'Đấu thầu rộng rãi'
            if review['bidForm'] == 'CHCTRG':
                review['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
            if review['bidForm'] == 'CDTRG':
                review['bidForm'] = 'Chỉ định thầu rút gọn'

        if review['isInternet'] is None:
            review['isInternet'] = ''
        if review['isInternet'] == 1:
            if review['bidForm'] == 'Đấu thầu rộng rãi' or review['bidForm'] == 'DTHC' or review['bidForm'] == 'MSTT':
                fee = '330,000 VND'
            elif review['bidForm'] == 'Chào hàng cạnh tranh' or review['bidForm'] == 'Chào hàng cạnh tranh rút gọn':
                fee = '220,000 VND'
        elif review['isInternet'] == 0:
            if review['feeValue'] is None:
                fee = ''
            else:
                fee = str(review['feeValue']) + 'VND'

        if review['notifyNo'] is None:
            review['notifyNo'] = ''

        if review['publicDate'] is None:
            review['publicDate'] = '0'

        if review['planNo'] is None:
            review['planNo'] = ''

        if review['planType'] is None:
            review['planType'] = ''
        else:
            if review['planType'] == 'DTPT':
                review['planType'] = 'Chi đầu tư phát triển'
            elif review['planType'] == 'TX':
                review['planType'] = 'Chi thường xuyên'

        if review['planName'] is None:
            review['planName'] = ''

        if review['bidName'] is None:
            review['bidName'] = ''

        if review['investorName'] is None:
            review['investorName'] = ''

        if review['procuringEntityName'] is None:
            review['procuringEntityName'] = ''

        if review['capitalDetail'] is None:
            review['capitalDetail'] = ''

        if review['investField'] is None:
            review['investField'] = ''

        if review['bidForm'] is None:
            review['bidForm'] = ''
        else:
            if review['bidForm'] == 'CHCT':
                review['bidForm'] = 'Chào hàng cạnh tranh'
            if review['bidForm'] == 'DTRR':
                review['bidForm'] = 'Đấu thầu rộng rãi'
            if review['bidForm'] == 'CHCTRG':
                review['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
            if review['bidForm'] == 'CDTRG':
                review['bidForm'] = 'Chỉ định thầu rút gọn'

        if review['isDomestic'] is None:
            review['isDomestic'] = ''
        else:
            if review['isDomestic'] == 1:
                review['isDomestic'] = 'Trong nước'
            elif review['isDomestic'] == 0:
                review['isDomestic'] = 'Quốc tế'

        if review['bidMode'] is None:
            review['bidMode'] = ''
        else:
            if review['bidMode'] == '1_MTHS':
                review['bidMode'] = 'Một giai đoạn một túi hồ sơ'
            elif review['bidMode'] == '1_HTHS':
                review['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

        if review['isInternet'] is None:
            review['isInternet'] = ''
        else:
            if review['isInternet'] == 1:
                review['isInternet'] = 'Qua mạng'
            elif review['isInternet'] == 0:
                review['isInternet'] = 'Không qua mạng'

        if review['issueLocation'] is None:
            review['issueLocation'] = ''

        if review['receiveLocation'] is None:
            review['receiveLocation'] = ''

        if review['bidCloseDate'] is None:
            review['bidCloseDate'] = ''

        if review['bidOpenDate'] is None:
            review['bidOpenDate'] = ''

        if review['bidOpenLocation'] is None:
            review['bidOpenLocation'] = ''

        if review['bidValidityPeriod'] is None:
            review['bidValidityPeriod'] = ''

        if review['bidValidityPeriodUnit'] is None:
            review['bidValidityPeriodUnit'] = ''
        x = str(review['bidValidityPeriod']) + ' ' + str(review['bidValidityPeriodUnit'])

        if json_data['bidInvContractorOfflineDTO'] is not None:
            if json_data['bidInvContractorOfflineDTO']['decisionNo'] is None:
                decisionNo = ''
            else:
                decisionNo = json_data['bidInvContractorOfflineDTO']['decisionNo']

            if json_data['bidInvContractorOfflineDTO']['decisionDate'] is None:
                decisionDate = ''
            else:
                decisionDate = json_data['bidInvContractorOfflineDTO']['decisionDate']

            if json_data['bidInvContractorOfflineDTO']['decisionAgency'] is None:
                decisionAgency = ''
            else:
                decisionAgency = json_data['bidInvContractorOfflineDTO']['decisionAgency']

            if json_data['bidInvContractorOfflineDTO']['decisionFileId'] is None:
                decisionFileId = ''
                link1 = ''
            else:
                decisionFileId = json_data['bidInvContractorOfflineDTO']['decisionFileId']
                link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + decisionFileId
        else:
            decisionNo = ''
            decisionDate = ''
            decisionAgency = ''
            decisionFileId = ''
            link1 = ''

        if review['id'] is None:
            review['id'] = ''
            link2 = ''
        else:
            link2 = 'https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=' + review['id']

        if review['bidPrice'] is None:
            review['bidPrice'] = ''
        if review2['bidoBidroundMngViewDTO'] is not None:
            if review2['bidoBidroundMngViewDTO']['successBidOpenDate'] is None:
                bien = ''
            else:
                bien = review2['bidoBidroundMngViewDTO']['successBidOpenDate']
            if review2['bidoBidroundMngViewDTO']['countContractor'] is not None:
                count = review2['bidoBidroundMngViewDTO']['countContractor']
        else:
            bien = ''

        if review['investField'] == "HH":
            review['investField'] = "Hàng hóa"
        elif review['investField'] == "PTV":
            review['investField'] = "Phi tư vấn"
        elif review['investField'] == "TV":
            review['investField'] = "Tư vấn"
        elif review['investField'] == "XL":
            review['investField'] = "Xây lắp"

        details.extend([
            review['notifyNo'],#0
            review['publicDate'],#1
            review["notifyVersion"],#2
            review['planNo'],#3
            review['planType'],#4
            review['planName'],#5
            review['bidName'],#6
            review['investorName'],#7
            review['procuringEntityName'],#8
            review['capitalDetail'],#9
            review['investField'],#10
            review['bidForm'],#11
            v,#12
            review['isDomestic'],#13
            review['bidMode'],#14
            a,#15
            review['isInternet'],#16
            review['issueLocation'],#17
            fee,#18
            review['receiveLocation'],#19
            b,#20
            review['bidCloseDate'],#21
            review['bidOpenDate'],#22
            review['bidOpenLocation'],#23
            str(review['bidValidityPeriod']) + str(review['bidValidityPeriodUnit']),#24
            decisionNo,#25
            decisionDate,#26
            decisionAgency,#27
            link1,#28
            link2,#29
            review['bidPrice'],#30
            dem,#31
            bien,#32
            nhap1,#33
            datesucces,#34
            ])
        
        bidType = upABN_db.bid_type(review['investField'])
        bidMethod = upABN_db.bid_method(review['isInternet'])
        crea_at = upABN_db.timeUpd()
        tim_open = upABN_db.time_close(review['bidOpenDate'])

        with open('' + folder_path1 + '/DXT.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)

        if upABN_db.ktTrungDL(review['notifyNo'], review["notifyVersion"]) == None:

            if details[10] == 'Tư vấn' or details[10] == 'TV':
                
                if mode == 'dsntdkt':

                    news_id = upABN_db.upDataDB_1_DXT_TV(7, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'], review["notifyVersion"])

                    open_result_status = 'complete_gd_hskt'
                    upABN_db.upDataDB_DXT_TV(tim_open, news_id,open_result_status)
                
                elif mode =='kqmt':

                    news_id = upABN_db.upDataDB_1_DXT_TV(7, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'], review["notifyVersion"])
                    
                    open_result_status = 'open_hskt_complete'
                    upABN_db.upDataDB_DXT_TV(tim_open, news_id,open_result_status)

                    upABNDetail_db.upData_DXT_TV(details, news_id)

                    upABO_db.upDataDB_TV(details, news_id)

            else:
                news_id = upABN_db.upDataDB_1_DXT(7, bidType, bidMethod, 1, crea_at, crea_at, review['notifyNo'], review["notifyVersion"])
                
                upABN_db.upDataDB_DXT(tim_open, news_id)

                upABNDetail_db.upData_DXT(details, news_id)

                upABO_db.upDataDB(details, news_id)

        details.clear()
        return news_id


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass
    return 'false'


def CrawlDetail_DT_DXT_TV_2(code, session1, codes, folder_path1, notify_no):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        '5321a273c51a75133e0fb1cd75e32e27': '90d57e96398dec0a2d505d16e8dab718',
        'JSESSIONID': 'j42sgmGH7hD0CrMTwBqHFE7zrzf6v-YAYv0pq7r4.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1678953886960',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1678952934.12.1.1678954032.0.0.0',
        'citrix_ns_id': 'AAY76skSZDvmstQAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==vdESZA==FJrG_ayohQqdZRWrr4alrzqYQOU=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; 5321a273c51a75133e0fb1cd75e32e27=90d57e96398dec0a2d505d16e8dab718; JSESSIONID=j42sgmGH7hD0CrMTwBqHFE7zrzf6v-YAYv0pq7r4.dc_app1_02; LFR_SESSION_STATE_20103=1678953886960; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1678952934.12.1.1678954032.0.0.0; citrix_ns_id=AAY76skSZDvmstQAAAAAADuFeyfrzB16Q6f2O1xwPpu7H2EZwZrlhyq0uv0rs0RgOw==vdESZA==FJrG_ayohQqdZRWrr4alrzqYQOU=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-2-kqmt&id=9506398d-3028-4735-9d7b-6a9b41f9540b&notifyId=9506398d-3028-4735-9d7b-6a9b41f9540b&inputResultId=undefined&bidOpenId=6207a849-263c-421d-a328-15cd627578d5&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=KHAC&bidMode=1_MTHS&notifyNo=IB2300037374&planNo=PL2300024675&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera GX";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/kqmt/bid-notify-contractor-out/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data = response.json()
        review = json_data
        nhap1 = []
        nhap1.clear()
        dem = 0
        data_dump = json.dumps(json_data)
        datesucces = ''
        if review is not None:
            if data_dump.find('bidoBidroundMngViewDTO') != -1:
                if review['bidoBidroundMngViewDTO'] is not None:
                    if review['bidoBidroundMngViewDTO']["successBidOpenDate"] is not None:
                        datesucces = review['bidoBidroundMngViewDTO']["successBidOpenDate"]

            if review['bidSubmissionByContractorViewResponse'] is not None:
                if review['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is not None:
                    for nhathau in review['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
                        if nhathau['contractorCode'] is None:
                            nhathau['contractorCode'] = ''

                        if nhathau['contractorName'] is None:
                            nhathau['contractorName'] = ''

                        if nhathau['bidPrice'] is None:
                            nhathau['bidPrice'] = ''

                        if nhathau['alternativeTech'] is None:
                            nhathau['alternativeTech'] = ''

                        if nhathau['bidFinalPrice'] is None:
                            nhathau['bidFinalPrice'] = ''

                        if nhathau['bidValidityNum'] is None:
                            nhathau['bidValidityNum'] = ''

                        if nhathau['bidGuarantee'] is None:
                            nhathau['bidGuarantee'] = ''

                        if nhathau['bidGuaranteeValidity'] is None:
                            nhathau['bidGuaranteeValidity'] = ''

                        if nhathau['contractPeriodDT'] is None:
                            nhathau['contractPeriodDT'] = ''

                        if nhathau['contractPeriodDTUnit'] is None:
                            nhathau['contractPeriodDTUnit'] = ''
                
                        nhap1.append([nhathau['contractorCode'],#0
                                      nhathau['contractorName'],#1
                                      nhathau['bidPrice'],#2
                                      nhathau['alternativeTech'],#3
                                      nhathau['bidFinalPrice'],#4
                                      nhathau['bidValidityNum'],#5
                                      nhathau['bidGuarantee'],#6
                                      nhathau['bidGuaranteeValidity'],#7
                                      str(nhathau['contractPeriodDT']) + nhathau['contractPeriodDTUnit']#8
                                      ])
                        dem = dem + 1

        return nhap1, dem, datesucces

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        j = "{}".format(notify_no)
        f.write("Ho so TBMT DXT 2 bi loi khong lay duoc du lieu: " + h + ', ma: ' + j)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass
    return

def CrawlDetail_DT_DXT_TV_DSNTDKT(code,details,session1,codes,folder_path1,notify_no,mode):
    
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        '5321a273c51a75133e0fb1cd75e32e27': '90d57e96398dec0a2d505d16e8dab718',
        'JSESSIONID': 'owDATgIVJ-YuugnyMw-nzYxCvTSkRN3goLdRNgDH.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1679540382420',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1679539415.4.1.1679541302.0.0.0',
        'citrix_ns_id': 'AAM7bbwbZDsCd90AAAAAADuFeyfrzB16Q6f2O3wkwp-X_KBiAk_jQriThj-xlt31Ow==wscbZA==QjeK8Pl9WuQtdK8A7YtYBQF0pos=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; 5321a273c51a75133e0fb1cd75e32e27=90d57e96398dec0a2d505d16e8dab718; JSESSIONID=owDATgIVJ-YuugnyMw-nzYxCvTSkRN3goLdRNgDH.dc_app1_02; LFR_SESSION_STATE_20103=1679540382420; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1679539415.4.1.1679541302.0.0.0; citrix_ns_id=AAM7bbwbZDsCd90AAAAAADuFeyfrzB16Q6f2O3wkwp-X_KBiAk_jQriThj-xlt31Ow==wscbZA==QjeK8Pl9WuQtdK8A7YtYBQF0pos=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-3-dsntdkt&id=0d5e9c20-57be-447d-9345-29644b92e55f&notifyId=0d5e9c20-57be-447d-9345-29644b92e55f&inputResultId=undefined&bidOpenId=2fa2e1bb-853b-48f6-b16d-eba57b8f00ae&techReqId=8184eab0-7f56-4397-a086-12b6c597ebe7&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_HTHS&notifyNo=IB2300021760&planNo=PL2300015190&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'sec-ch-ua': '"Not=A?Brand";v="8", "Chromium";v="110", "Opera GX";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    
    try:
        news_id = CrawlDetail_DT_DXT_TV_KQMT(code,details,session1,codes,folder_path1,notify_no,mode)
        if news_id == 'false':
            news_id = 0

        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"8184eab0-7f56-4397-a086-12b6c597ebe7"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/ldtdsnt/tech-req-approval/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify= False,
            timeout=30,
        )
        json_data = response.json()
        data = json.dumps(json_data)
        if json_data is not None:
            if json_data['bidNoContractorResponse'] is not None:
                if json_data['bidNoContractorResponse']['bidNotification'] is not None:
                    review1 = json_data['bidNoContractorResponse']['bidNotification']

            if json_data['bidrTechReqApprovalDTO'] is not None:
                if json_data['bidrTechReqApprovalDTO']['bidReqApprovalDetail'] is not None:
                    review2 = json_data['bidrTechReqApprovalDTO']['bidReqApprovalDetail']
                
            if json_data['lsBideLotEvalResultViewDTO'] is not None:
                dsnt = json_data['lsBideLotEvalResultViewDTO']

        if review1['bidNo'] is None:
            review1 ['bidNo'] = ''

        if review1['status'] is None:
            review1['status'] = ''
        else:
            if review1['status'] == '01':
                review1['status'] = 'Đã đăng tải'
        
        if review1['procuringEntityName'] is None:
            review1['procuringEntityName'] = ''

        if review1['investorName'] is None:
            review1['investorName'] = ''
        
        if review1['bidName'] is None:
            review1['bidName'] = ''
        
        if review1['bidPrice'] is None:
            review1['bidPrice'] = ''
        
        if review1['bidEstimatePrice'] is None:
            review1['bidEstimatePrice'] = ''

        if review1['contractType'] is None:
            review1['contractType'] = ''
        else:
            if review1['contractType'] == 'TG':
                review1['contractType'] = 'Trọn gói'

        if review1['bidForm'] is None:
            review1['bidForm'] = ''
        else:
            if review1['bidForm'] == 'CHCT':
                review1['bidForm']  = 'Chào hàng cạnh tranh'
            if review1['bidForm'] == 'DTRR':
                review1['bidForm']  = 'Đấu thầu rộng rãi'
            if review1['bidForm'] == 'CHCTRG':
                review1['bidForm']  = 'Chào hàng cạnh tranh rút gọn'
            if review1['bidForm'] == 'CDTRG':
                review1['bidForm']  = 'Chỉ định thầu rút gọn'

        if review1['bidMode'] is None:
            review1['bidMode'] = ''
        else:
            if review1['bidMode'] == '1_MTHS':
                review1['bidMode'] = 'Một giai đoạn một túi hồ sơ'
            elif review1['bidMode'] == '1_HTHS':
                review1['bidMode'] = 'Một giai đoạn hai túi hồ sơ'

        if review1['investField'] is None:
            review1['investField'] = ''
        else:
            if review1['investField'] == 'TV':
                review1['investField'] = 'Tư vấn'

        if review1['capitalDetail'] is None:
            review1['capitalDetail'] = ''
        
        if review1['isDomestic'] is None:
            review1['isDomestic'] = ''
        else:
            if review1['isDomestic'] == 1 or review1['isDomestic'] == '1':
                review1['isDomestic'] = 'Trong nước'
            else:
                review1['isDomestic'] = 'Quốc tế'

        if review1['contractPeriod'] is None:
            contractPeriod = ''
        else:
            if review1['contractPeriodUnit'] is None:
                contractPeriod = ''
            else:
                if review1['contractPeriodUnit'] == 'D':
                    review1['contractPeriodUnit'] = 'ngày'
                elif review1['contractPeriodUnit'] == 'M':
                    review1['contractPeriodUnit'] = 'tháng'
                contractPeriod = str(review1['contractPeriodUnit']) + ' '+ review1['contractPeriodUnit']

        if review2['approvalDate'] is None:
            review2['approvalDate'] = ''
        
        if review2['decisionNo'] is None:
            review2['decisionNo'] =''

        if review2['decisionAgencyName'] is None:
            review2['decisionAgencyName'] =''

        if review2['decisionFileName'] is None:
            review2['decisionFileName'] =''

        if review2['decisionFileId'] is None:
            link = ''
        else:
            link = 'http://localhost:1234/api/download/file/browser/public?fileId='+review2['decisionFileId']
        details.clear
        reason = ''
        list_nt_pass = []
        list_nt_no_pass = []
        MAP_EVAL_TYPE=[('1','Nhà thầu không đạt tại bước Đánh giá Tính hợp lệ'),
        ('2','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm'),
        ('3', 'Nhà thầu không đạt tại bước Đánh giá Kỹ thuật'),
        ('5','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm (Nhân sự chủ chốt)'),
        ('6','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm (Thiết bị thi công)'),
        ('5,6','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm (Nhân sự chủ chốt và thiết bị thi công)'),
        ('2,5,6','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm, Nhân sự chủ chốt, thiết bị thi công'),
        ('2,5','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm, Nhân sự chủ chốt'),
        ('2,6','Nhà thầu không đạt tại bước Đánh giá Năng lực kinh nghiệm, thiết bị thi công')]
        
        demnt=0
        demnt_pass=0
        demnt_fail_kt=0
        demnt_fail_khac=0
        for nt in dsnt:
            if nt['result'] is None:
                nt['result'] = ''
            if nt['result'] == '2' or nt['result'] == 0:
                demnt = demnt+1
                if nt['evalType'] == 3 and nt['result'] == '2':
                    if nt['contractorCode'] is None:
                        nt['contractorCode'] = ''
                    
                    if nt['contractorName'] is None:
                        nt['contractorName'] = ''

                    if nt['techScore'] is None:
                        nt['techScore'] = ''
                    demnt_pass=demnt_pass+1
                    
                    list_nt_pass.append([nt['contractorCode'],nt['contractorName'],nt['techScore'],contractPeriod,'Đạt yêu cầu kỹ thuật'])
                
                if nt['result'] == 0:
                    if nt['contractorCode'] is None:
                        nt['contractorCode'] = ''
                    
                    if nt['contractorName'] is None:
                        nt['contractorName'] = ''

                    if nt['techScore'] is None:
                        nt['techScore'] = ''

                    if nt['evalType'] is None:
                        nt['evalType']=''
                    else:
                        for i in MAP_EVAL_TYPE:
                            if nt['evalType'] == i[0]:
                                reason = i[1]
                                if i[0] == 3 or i[0]=='3':
                                    demnt_fail_kt = demnt_fail_kt + 1
                                else:
                                    demnt_fail_khac = demnt_fail_khac + 1
                                list_nt_no_pass.append([nt['contractorCode'],nt['contractorName'],nt['techScore'],contractPeriod,reason])   
                        reason=''      
        
        details=[]
        details.append([review1['bidNo'],#0
                        review1['status'],#1
                        review1['procuringEntityName'],#2
                        review1['investorName'],#3
                        review1['bidName'],#4
                        review1['bidPrice'],#5
                        review1['bidEstimatePrice'],#6
                        review1['contractType'],#7
                        review1['bidForm'],#8
                        review1['bidMode'],#9
                        review1['investField'],#10
                        review1['capitalDetail'],#11
                        review1['isDomestic'],#12
                        contractPeriod,#13
                        review2['approvalDate'],#14
                        review2['decisionNo'],#15
                        review2['decisionAgencyName'],#16
                        review2['decisionFileName'],#17
                        link,#18
                        list_nt_pass,#19
                        list_nt_no_pass,#20
                        demnt,#21
                        demnt_pass,#22
                        demnt_fail_khac,#23
                        demnt_fail_kt])#24
        
        updata_DSNTDKT(news_id,details)
        
    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open(''+folder_path1+"/log.txt", "a")
        h="{}".format(code)
        j="{}".format(notify_no)
        f.write("Ho so TBMT DXT DSNTDKT bi loi khong lay duoc du lieu: "+ h +', ma: '+j)
        f.write('\n')
        f.close()
        i = random.randrange(1,10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open(''+folder_path1+"/log.txt", "a")
        h="{}".format(code)
        j="{}".format(notify_no)
        f.write("Ho so TBMT DXT DSNTDKT bi loi khong lay duoc du lieu: "+ h +', ma: '+j)
        f.write('\n')
        f.close()
        i = random.randrange(1,10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open(''+folder_path1+"/log.txt", "a")
        h="{}".format(code)
        j="{}".format(notify_no)
        f.write("Ho so TBMT DXT DSNTDKT bi loi khong lay duoc du lieu: "+ h +', ma: '+j)
        f.write('\n')
        f.close()
        i = random.randrange(1,10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open(''+folder_path1+"/log.txt", "a")
        h="{}".format(code)
        j="{}".format(notify_no)
        f.write("Ho so TBMT DXT DSNTDKT bi loi khong lay duoc du lieu: "+ h +', ma: '+j)
        f.write('\n')
        f.close()
        i = random.randrange(1,10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass
    return

def updata_DSNTDKT(news_id,details):
    so_tbmt = details[0]
    ten_goi_thau = details[4]
    loai_hop_dong = details[7]
    phuong_thuc = details[9]
    tong_so_nha_thau_tham_du = details[21]
    nha_thau_dap_ung_2 = details[22]
    nha_thau_khong_dap_ung_2 = details[24]
    
    nha_thau_khong_dap_ung_1 = details[23]
    nha_thau_dap_ung_1 = int(tong_so_nha_thau_tham_du) - int(nha_thau_khong_dap_ung_1)
    
    sub_title1 = 'Thông tin gói thầu'
    titles1 = 'Số TBMT'
    titles2 = 'Tên gói thầu'
    titles3 = 'Loại hợp đồng'
    titles4 = 'Phương thức'

    sub_title2='Thông tin thống kê'
    titles5 = 'Tổng số nhà thầu tham dự'
    titles6 = 'Nhà thầu đáp ứng'
    titles7 = 'Nhà thầu không đáp ứng'
    titles8 = 'Nhà thầu đáp ứng'
    titles9 = 'Nhà thầu không đáp ứng'

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

    value1 = so_tbmt
    value2 = ten_goi_thau
    value3 = loai_hop_dong
    value4 = phuong_thuc
    value5 = tong_so_nha_thau_tham_du
    value6 = nha_thau_dap_ung_1
    value7 = nha_thau_khong_dap_ung_1
    value8 = nha_thau_dap_ung_2
    value9 = nha_thau_khong_dap_ung_2
    type_id = 7
    records = [(key1,sub_title1,titles1,value1,news_id,type_id),
               (key2,sub_title1,titles2,value2,news_id,type_id),
               (key3,sub_title1,titles3,value3,news_id,type_id),
               (key4,sub_title1,titles4,value4,news_id,type_id),
               (key5,sub_title2,titles5,value5,news_id,type_id),
               (key6,sub_title2,titles6,value6,news_id,type_id),
               (key7,sub_title2,titles7,value7,news_id,type_id),
               (key8,sub_title2,titles8,value8,news_id,type_id),
               (key9,sub_title2,titles9,value9,news_id,type_id)]
    
    conn = connectdb.connect()
    cur = conn.cursor()
    sql1 = "INSERT INTO pccc_app_bidding_news_details (`key`, sub_title, title, value, news_id, type_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW());"
    cur.executemany(sql1, records)
    conn.commit()

def CrawlDetail_DT_CNTTT(code, details, session1, codes, folder_path1, code1, code2):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'JSESSIONID': 'P8qD1trpOCbKugcHzLUSfc-EJmmDFcU45yMx_Oyr.dc_app1_02',
        'LFR_SESSION_STATE_20103': '1677295548357',
        '_ga_19996Z37EE': 'GS1.1.1677292879.41.1.1677295564.0.0.0',
        'citrix_ns_id': 'AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==XIP5Yw==yAwzuDLaKsNxiKG6oLupFM7gZGE=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; JSESSIONID=P8qD1trpOCbKugcHzLUSfc-EJmmDFcU45yMx_Oyr.dc_app1_02; LFR_SESSION_STATE_20103=1677295548357; _ga_19996Z37EE=GS1.1.1677292879.41.1.1677295564.0.0.0; citrix_ns_id=AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==XIP5Yw==yAwzuDLaKsNxiKG6oLupFM7gZGE=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=IB2300026250&notifyId=IB2300026250&inputResultId=b8b48175-5c43-44b2-8590-2ca48a15db5f&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=undefined&notifyNo=IB2300026250&planNo=undefined&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    try:
        dem = 0
        nhap1 = [0]
        nhap1.clear()
        bien = 0
        nhap1, bien, dem = CrawDetail_DT_CNTTT_1(notifyNo=code1, session1=session1, folder_path1=folder_path1, dem=dem)

        nhap2 = [0]
        nhap2.clear()
        nhap2, decisionCNTTT, listHangHoa, listLienDanh = CrawDetail_DT_CNTTT_2(inputResultId=code2, session1=session1, folder_path1=folder_path1, nhap2=nhap2)
        # Request theo id trong list_TBMT_CDT de lay cac thong tin cho vao CT_TBMT_CDT
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bido-notify-contractor-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data1 = response.json()
        if json_data1 is not None:
            data = json.dumps(json_data1)
            if data.find('bidoNotifyContractorP') != -1:
                if json_data1['bidoNotifyContractorP'] is not None:
                    review1 = json_data1['bidoNotifyContractorP']
                    if review1['cPeriod'] is None:
                        review1['cPeriod'] = 0
                    if review1['cPeriodUnit'] is None:
                        review1['cPeriodUnit'] = 0
                    a = str(review1['cPeriod']) + str(review1['cPeriodUnit'])
                    if review1['cType'] is not None:
                        v = review1['cType']
                    else:
                        v = 0

            elif data.find('bidoNotifyContractorM') != -1:
                if json_data1['bidoNotifyContractorM'] is not None:
                    review1 = json_data1['bidoNotifyContractorM']
                    if review1['contractPeriod'] is None:
                        review1['contractPeriod'] = 0
                    if review1['contractPeriodUnit'] is None:
                        review1['contractPeriodUnit'] = 0
                    a = str(review1['contractPeriod']) + str(review1['contractPeriodUnit'])
                    if review1['contractType'] is not None:
                        v = review1['contractType']
                    else:
                        v = 0

        if data.find('bidpBidLocationList') != -1:
            if json_data1['bidpBidLocationList'] is None:
                b = 0
            else:
                if json_data1['bidpBidLocationList'][0] is not None:
                    if json_data1['bidpBidLocationList'][0]['districtName'] is None:
                        b = json_data1['bidpBidLocationList'][0]['provName']
                    elif json_data1['bidpBidLocationList'][0]['provName'] is None:
                        b = json_data1['bidpBidLocationList'][0]['districtName']
                    else:
                        b = json_data1['bidpBidLocationList'][0]['districtName'] + ", " + \
                            json_data1['bidpBidLocationList'][0]['provName']

        elif data.find('lsBidpBidLocationDTO') != -1:
            if json_data1['lsBidpBidLocationDTO'] is None:
                b = 0
            else:
                if json_data1['lsBidpBidLocationDTO'][0] is not None:
                    if json_data1['lsBidpBidLocationDTO'][0]['districtName'] is None:
                        b = json_data1['lsBidpBidLocationDTO'][0]['provName']
                    elif json_data1['lsBidpBidLocationDTO'][0]['provName'] is None:
                        b = json_data1['lsBidpBidLocationDTO'][0]['districtName']
                    else:
                        b = json_data1['lsBidpBidLocationDTO'][0]['districtName'] + ", " + \
                            json_data1['lsBidpBidLocationDTO'][0]['provName']

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

        if review1['publicDate'] is None:
            review1['publicDate'] = 0

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
                bidForm = 'Chào hàng cạnh tranh'
            if review1['bidForm'] == 'DTRR':
                bidForm = 'Đấu thầu rộng rãi'
            if review1['bidForm'] == 'CHCTRG':
                bidForm = 'Chào hàng cạnh tranh rút gọn'
            if review1['bidForm'] == 'CDTRG':
                bidForm = 'Chỉ định thầu rút gọn'

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

        if review1['issueLocation'] is None:
            review1['issueLocation'] = 0

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

        if review1['guaranteeValue'] is None:
            review1['guaranteeValue'] = 0

        if review1['guaranteeForm'] is None:
            review1['guaranteeForm'] = 0

        if json_data1['bidInvContractorOfflineDTO'] is not None:
            if json_data1['bidInvContractorOfflineDTO']['decisionNo'] is None:
                decisionNo = 0
            else:
                decisionNo = json_data1['bidInvContractorOfflineDTO']['decisionNo']

            if json_data1['bidInvContractorOfflineDTO']['decisionDate'] is None:
                decisionDate = 0
            else:
                decisionDate = json_data1['bidInvContractorOfflineDTO']['decisionDate']

            if json_data1['bidInvContractorOfflineDTO']['decisionAgency'] is None:
                decisionAgency = 0
            else:
                decisionAgency = json_data1['bidInvContractorOfflineDTO']['decisionAgency']

            if json_data1['bidInvContractorOfflineDTO']['decisionFileId'] is not None:
                link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + \
                        json_data1['bidInvContractorOfflineDTO']['decisionFileId'],
            else:
                link1 = 0
        else:
            decisionNo = 0
            decisionDate = 0
            decisionAgency = 0
            link1 = 0

        if review1['notifyVersion'] is None:
            review1['notifyVersion'] = ''

        if review1['id'] is not None:
            link2 = 'https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=' + review1['id'],
        else:
            link2 = 0
        if review1['bidPrice'] is None:
            review1['bidPrice'] = 0
        details.extend([review1['notifyNo'],
                        review1['publicDate'],
                        review1["notifyVersion"],  # 2
                        review1['planNo'],
                        review1['planType'],
                        review1['planName'],
                        review1['bidName'],
                        review1['investorName'],
                        review1['procuringEntityName'],
                        review1['capitalDetail'],
                        review1['investField'],
                        bidForm,
                        v,
                        review1['isDomestic'],
                        review1['bidMode'],
                        a,
                        review1['isInternet'],
                        review1['issueLocation'],
                        fee,
                        review1['receiveLocation'],
                        b,
                        review1['bidCloseDate'],
                        review1['bidOpenDate'],
                        review1['bidOpenLocation'],
                        str(review1['bidValidityPeriod']) + str(review1['bidValidityPeriodUnit']),
                        review1['guaranteeValue'],
                        review1['bidPrice'],
                        review1['guaranteeForm'],
                        decisionNo,
                        decisionDate,
                        decisionAgency,
                        link1,
                        link2,
                        dem,
                        bien,
                        nhap1,
                        nhap2,
                        codes,
                        decisionCNTTT,
                        listLienDanh,
                        listHangHoa])
        bidType = upABN_db.bid_type(details[10])
        bidMethod = upABN_db.bid_method(details[16])
        crea_at = upABN_db.timeUpd()
        tim_close = upABN_db.time_close(details[21])
        time_post = upABN_db.time_post(details[1])
        date_app = upABN_db.date_app2(decisionDate)
        news_id = 0
        if upABN_db.ktTrungDL(review1['notifyNo'], review1["notifyVersion"]) == None:
            news_id = upABN_db.upDataDB(8, bidType, bidMethod, 1, crea_at, crea_at, review1['notifyNo'],
                                        review1["notifyVersion"],
                                        tim_close, time_post, date_app)
            upABNDetail_db.upData_CNTTT(details, news_id)
            upABO_result_complete_gd_hsdt.upData(details, news_id, 1)
            # print(f"ListHH ---- {listHangHoa}")
            if listHangHoa != []:
                upABRGoods_db.upData_CNTTT(listHangHoa, news_id)
            up_ABN_joint_ventures_db.upData_CNTTT(listLienDanh, news_id, 8)
            # print(1)

        with open('' + folder_path1 + '/CNTTT.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()
        return


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass


def CrawDetail_DT_CNTTT_1(notifyNo, session1, folder_path1, dem):
    cookies2 = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': '2M0FtYPE249N-JxE30p-BxDAclmuUln5yBJKNNIQ.dc_app1_01',
        'LFR_SESSION_STATE_20103': '1676788514796',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        '_ga_19996Z37EE': 'GS1.1.1676788070.5.1.1676789211.0.0.0',
        'citrix_ns_id': 'AAE7ar_xYzvrK64AAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==YsnxYw==x_2EGEljGY2abWHfUM_y5bDiYlY=',
    }

    headers2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=2M0FtYPE249N-JxE30p-BxDAclmuUln5yBJKNNIQ.dc_app1_01; LFR_SESSION_STATE_20103=1676788514796; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1676788070.5.1.1676789211.0.0.0; citrix_ns_id=AAE7ar_xYzvrK64AAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==YsnxYw==x_2EGEljGY2abWHfUM_y5bDiYlY=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=8051e056-f3b3-4318-bf09-baa91ee3d95d&notifyId=8051e056-f3b3-4318-bf09-baa91ee3d95d&inputResultId=eaf045bc-91fe-4e5d-a02e-fea93bb1bb90&bidOpenId=eafe7066-9c56-4db7-a642-42e7c4674d11&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300018722&planNo=PL2300014693&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data2 = '{"notifyNo":"' + notifyNo + '","type":"TBMT","packType":0}'
        response2 = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/ldtkqmt/bid-notification-p/get-by-id',
            cookies=cookies2,
            headers=headers2,
            data=data2,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data2 = response2.json()
        review2 = json_data2
        nhap1 = [0]
        nhap1.clear()
        if review2 is None:
            return 0, 0, 0
        else:
            if review2['bidSubmissionByContractorViewResponse'] is None:
                return 0, 0, 0
            else:
                if review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is None:
                    return 0, 0, 0
                if review2['bidoBidroundMngViewDTO']['successBidOpenDate'] is None:
                    review2['bidoBidroundMngViewDTO']['successBidOpenDate'] = 0

        for nhathau in review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
            if nhathau['contractorCode'] is None:
                nhathau['contractorCode'] = 0

            if nhathau['contractorName'] is None:
                nhathau['contractorName'] = 0

            if nhathau['bidPrice'] is None:
                nhathau['bidPrice'] = 0

            if nhathau['alternativeTech'] is None:
                nhathau['alternativeTech'] = 0

            if nhathau['bidFinalPrice'] is None:
                nhathau['bidFinalPrice'] = 0

            if nhathau['bidValidityNum'] is None:
                nhathau['bidValidityNum'] = 0

            if nhathau['bidGuarantee'] is None:
                nhathau['bidGuarantee'] = 0

            if nhathau['bidGuaranteeValidity'] is None:
                nhathau['bidGuaranteeValidity'] = 0

            if nhathau['contractPeriodDT'] is None:
                nhathau['contractPeriodDT'] = 0

            if nhathau['contractPeriodDTUnit'] is None:
                nhathau['contractPeriodDTUnit'] = 0

            nhap1.append(
                [nhathau['contractorCode'], nhathau['contractorName'], nhathau['bidPrice'], nhathau['alternativeTech'],
                 nhathau['bidFinalPrice'], nhathau['bidValidityNum'], nhathau['bidGuarantee'],
                 nhathau['bidGuaranteeValidity'],
                 str(nhathau['contractPeriodDT']) + str(nhathau['contractPeriodDTUnit'])])
            dem = dem + 1

        return nhap1, review2['bidoBidroundMngViewDTO']['successBidOpenDate'], dem


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(notifyNo)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(notifyNo)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(notifyNo)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(notifyNo)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass


def CrawDetail_DT_CNTTT_2(inputResultId, session1, folder_path1, nhap2):
    cookies3 = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'LFR_SESSION_STATE_20103': '1677299771614',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'JSESSIONID': 'j32Jyt6aLSDjzUCPbJ54aLZszP5dzJwMXAj-_n7i.dc_app1_02',
        '_ga_19996Z37EE': 'GS1.1.1677302324.43.1.1677302340.0.0.0',
        'citrix_ns_id': 'AAQ7MZr5YzucIbwAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==y535Yw==exYEMKTSv390EFm78JcEbK4CM14=',
    }

    headers3 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1677299771614; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; JSESSIONID=j32Jyt6aLSDjzUCPbJ54aLZszP5dzJwMXAj-_n7i.dc_app1_02; _ga_19996Z37EE=GS1.1.1677302324.43.1.1677302340.0.0.0; citrix_ns_id=AAQ7MZr5YzucIbwAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==y535Yw==exYEMKTSv390EFm78JcEbK4CM14=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=aca05bb6-40b7-43a7-b4f8-9fcb5ddb9097&notifyId=aca05bb6-40b7-43a7-b4f8-9fcb5ddb9097&inputResultId=a313cf55-5bc5-4003-9cb4-8fde3e4dc2ad&bidOpenId=00e4e371-cb82-4d7a-8cca-b432cceb9580&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300023119&planNo=PL2300018300&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data3 = '{"id":"' + inputResultId + '"}'
        response3 = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/contractor-input-result/get',
            cookies=cookies3,
            headers=headers3,
            data=data3,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )

        json_data3 = response3.json()
        review3 = json_data3
        nhap2 = [0]
        nhap2.clear()
        if review3 is None:
            return
        else:
            if review3['bideContractorInputResultDTO'] is None:
                return
            else:
                if review3['bideContractorInputResultDTO']['lotResultDTO'] is None:
                    return
                else:
                    if review3['bideContractorInputResultDTO']['lotResultDTO'][0] is None:
                        return
                    else:
                        if review3['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList'] is None:
                            return
        if review3['bideContractorInputResultDTO']['decisionDate'] is  None:
            review3['bideContractorInputResultDTO']['decisionDate'] =''

        for nhathau in review3['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList']:
            if nhathau['orgCode'] is None:
                nhathau['orgCode'] = 0

            if nhathau['orgFullname'] is None:
                nhathau['orgCode'] = 0

            if nhathau['lotFinalPrice'] is None:
                nhathau['orgCode'] = 0

            if nhathau['bidWiningPrice'] is None:
                nhathau['orgCode'] = 0

            if nhathau['cperiod'] is None:
                nhathau['orgCode'] = 0

            if nhathau['cperiodUnit'] is None:
                nhathau['orgCode'] = 0

            if nhathau['bidResult'] is None:
                nhap2.append([nhathau['orgCode'], nhathau['orgFullname'], nhathau['reason'], 0, 0])

            elif nhathau['bidResult'] == 1:
                nhap2.append(
                    [nhathau['orgCode'], nhathau['orgFullname'], nhathau['lotFinalPrice'], nhathau['bidWiningPrice'],
                     str(nhathau['cperiod']) + nhathau['cperiodUnit']])

        return nhap2,  review3['bideContractorInputResultDTO']['decisionDate'], crawlDetail_HangHoa_CNTTT(review3), LienDanh.liendanh(review3)
    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass


def CrawDetail_DT_CNTTT_KQM(inputResultId, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'JSESSIONID': 'EjKa8X-ItOKYz3qrc56vTR8hRaJnyjC3AtCO45_o.dc_app1_01',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
        'LFR_SESSION_STATE_20103': '1677296447665',
        '_ga_19996Z37EE': 'GS1.1.1677292879.41.1.1677296463.0.0.0',
        'citrix_ns_id': 'AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==3ob5Yw==lBkRIhhcwjXAP8AyH8OfnzTA8ow=',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=EjKa8X-ItOKYz3qrc56vTR8hRaJnyjC3AtCO45_o.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677296447665; _ga_19996Z37EE=GS1.1.1677292879.41.1.1677296463.0.0.0; citrix_ns_id=AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==3ob5Yw==lBkRIhhcwjXAP8AyH8OfnzTA8ow=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=IB2300024175&notifyId=IB2300024175&inputResultId=2aad6a2a-cff4-43a8-8a8e-93c576c05867&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=undefined&notifyNo=IB2300024175&planNo=undefined&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
        'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        i = random.randrange(1,10)
        time.sleep(i)
        session = session1
        data = '{"id":"' + inputResultId + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/contractor-input-result/get',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data1 = response.json()
        if json_data1 is None:
            return
        else:
            if json_data1['bideContractorInputResultDTO'] is not None:
                review1 = json_data1['bideContractorInputResultDTO']
            if json_data1['bidpPlanDetailDTO'] is not None:
                review2 = json_data1['bidpPlanDetailDTO']

        if review1['notifyNo'] is None:
            review1['notifyNo'] = 0

        if review1['publicDate'] is None:
            review1['publicDate'] = 0

        if review1['investorName'] is None:
            review1['investorName'] = 0

        if review2['planNo'] is None:
            review2['planNo'] = 0

        if review1['bidName'] is None:
            review1['bidName'] = 0

        if review1['bidEstimatePrice'] is None:
            review1['bidEstimatePrice'] = 0

        if review1['bidPrice'] is None:
            review1['bidPrice'] = 0

        if review1['ctype'] is None:
            review1['ctype'] = 0

        if review1['bidForm'] is None:
            review1['bidForm'] = 0

        if review1['bidMode'] is None:
            review1['bidMode'] = 0

        if review1['bidField'] is None:
            review1['bidField'] = 0

        if review1['decisionDate'] is None:
            review1['decisionDate'] = 0

        if review1['decisionAgency'] is None:
            review1['decisionAgency'] = 0

        if review1['decisionNo'] is None:
            review1['decisionNo'] = 0

        if review1['reportFileId'] is None:
            link1 = 0
        else:
            link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + review1['reportFileId']

        if review1['isDomestic'] is None:
            review1['isDomestic'] = ''
        else:
            if review1['isDomestic'] == 1 or review1['isDomestic'] == True:
                review1['isDomestic'] = 'Trong nước'
            else:
                review1['isDomestic'] = 'Quốc tế'

        nhap = [0]
        nhap.clear()
        if review1['lotResultDTO'] is not None:
            if review1['lotResultDTO'][0] is not None:
                if review1['lotResultDTO'][0]['contractorList'] is not None:
                    for nhathau in review1['lotResultDTO'][0]['contractorList']:
                        if nhathau['bidResult'] == 1:
                            if nhathau['orgCode'] is None:
                                nhathau['orgCode'] = 0

                            if nhathau['orgFullname'] is None:
                                nhathau['orgFullname'] = 0

                            if nhathau['bidWiningPrice'] is None:
                                nhathau['bidWiningPrice'] = 0

                            nhap.append([nhathau['orgCode'], nhathau['orgFullname'], nhathau['bidWiningPrice']])
        details.clear()
        details.extend(
            [review1['notifyNo'], review1['publicDate'], review1['investorName'], review2['planNo'], review1['bidName'],
             review1['bidEstimatePrice'], review1['bidPrice'], review1['ctype'], review1['bidForm'], review1['bidMode'],
             review1['bidField'], review1['decisionDate'], review1['decisionAgency'], review1['decisionNo'], link1,
             review1['isDomestic'], nhap, codes])
        
        with open('' + folder_path1 + '/CNTTT_KQM.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
            details.clear()


    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.exceptions.ConnectionError:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(inputResultId)
        f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        pass
    return


def CrawlDetail_DT_DHT(code, details, session1, codes, folder_path1):
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'vi_VN',
        '_ga': 'GA1.1.2001033887.1675655198',
        'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
        '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
        '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
        '_ga_19996Z37EE': 'deleted',
        '_ga_19996Z37EE': 'deleted',
        'LFR_SESSION_STATE_20103': '1676806960147',
        'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
        'JSESSIONID': 'sPuYvBkwDkZypitmTdpBnEQ30_ssO2dBJ-cmV5J4.dc_app1_02',
        '_ga_19996Z37EE': 'GS1.1.1676800384.7.1.1676807287.0.0.0',
        'citrix_ns_id': 'AAU7dQryYzvKpa8AAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==_Q_yYw==8nseYrgWcGouXKO4AZYsG46wCG4=',
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1676806960147; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; JSESSIONID=sPuYvBkwDkZypitmTdpBnEQ30_ssO2dBJ-cmV5J4.dc_app1_02; _ga_19996Z37EE=GS1.1.1676800384.7.1.1676807287.0.0.0; citrix_ns_id=AAU7dQryYzvKpa8AAAAAADuFeyfrzB16Q6f2Ow-WzuZW1OVoEc-PiPO9Fxb-dn0lOw==_Q_yYw==8nseYrgWcGouXKO4AZYsG46wCG4=',
        'Origin': 'https://muasamcong.mpi.gov.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-1-tbmt&id=1e6cf4ba-b740-45ac-8ce1-6b54073f9798&notifyId=1e6cf4ba-b740-45ac-8ce1-6b54073f9798&inputResultId=undefined&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300018230&planNo=PL2300014233&pno=undefined',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
        'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        # Request theo id trong list_TBMT_CDT de lay cac thong tin cho vao CT_TBMT_CDT
        session = session1
        i = random.randrange(1,10)
        time.sleep(i)
        data = '{"id":"' + code + '"}'
        response = session.post(
            'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bido-notify-contractor-view/get-by-id',
            cookies=cookies,
            headers=headers,
            data=data,
            allow_redirects=False,
            verify=False,
            timeout=30,
        )
        json_data1 = response.json()

        data = json.dumps(json_data1)
        if json_data1 is not None:
            data = json.dumps(json_data1)
            if data.find('bidoNotifyContractorP') != -1:
                if json_data1['bidoNotifyContractorP'] is not None:
                    review1 = json_data1['bidoNotifyContractorP']
                    if review1['cPeriod'] is None:
                        review1['cPeriod'] = 0
                    if review1['cPeriodUnit'] is None:
                        review1['cPeriodUnit'] = 0
                    a = str(review1['cPeriod']) + str(review1['cPeriodUnit'])
                    if review1['cType'] is not None:
                        v = review1['cType']
                    else:
                        v = 0

            elif data.find('bidoNotifyContractorM') != -1:
                if json_data1['bidoNotifyContractorM'] is not None:
                    review1 = json_data1['bidoNotifyContractorM']
                    if review1['contractPeriod'] is None:
                        review1['contractPeriod'] = 0
                    if review1['contractPeriodUnit'] is None:
                        review1['contractPeriodUnit'] = 0
                    a = str(review1['contractPeriod']) + str(review1['contractPeriodUnit'])
                    if review1['contractType'] is not None:
                        v = review1['contractType']
                    else:
                        v = 0

        if review1['notifyNo'] is None:
            review1['notifyNo'] = 0

        if review1['publicDate'] is None:
            review1['publicDate'] = 0

        if review1['planNo'] is None:
            review1['planNo'] = 0

        if review1['planType'] is None:
            review1['planType'] = 0

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

        if review1['investField'] is None:
            review1['investField'] = 0

        if review1['bidForm'] is None:
            review1['bidForm']

        if review1['isDomestic'] is None:
            review1['isDomestic'] = ''
        else:
            if review1['isDomestic'] == 1 or review1['isDomestic'] == True:
                review1['isDomestic'] = 'Trong nước'
            else:
                review1['isDomestic'] = 'Quốc tế'

        if review1['bidMode'] is None:
            review1 = 0

        if review1['isInternet'] is None:
            review1['isInternet'] = 0
        else:
            if review1['isInternet'] == 1 or review1['isInternet'] == True:
                review1['isInternet'] = 'Qua mạng'
            else:
                review1['isInternet'] = 'Không qua mạng'

        if review1['issueLocation'] is None:
            review1['issueLocation'] = 0

        fee = 0
        if review1['bidForm'] is None:
            review1['bidForm'] = 0
        if review1['isInternet'] is None:
            review1['isInternet'] = 0
        else:
            if review1['isInternet'] == 1:
                if review1['bidForm'] == 'DTRR' or review1['bidForm'] == 'DTHC' or review1['bidForm'] == 'MSTT':
                    fee = '330,000 VND'
                elif review1['bidForm'] == 'CHCT' or review1['bidForm'] == 'CHCTRG':
                    fee = '220,000 VND'
            elif review1['isInternet'] == 0:
                if review1['feeValue'] is None:
                    fee = ''
                else:
                    fee = str(review1['feeValue']) + 'VND'

        if data.find('bidpBidLocationList') != -1:
            if json_data1['bidpBidLocationList'] is None:
                b = 0
            else:
                if json_data1['bidpBidLocationList'][0] is not None:
                    if json_data1['bidpBidLocationList'][0]['districtName'] is None:
                        b = json_data1['bidpBidLocationList'][0]['provName']
                    elif json_data1['bidpBidLocationList'][0]['provName'] is None:
                        b = json_data1['bidpBidLocationList'][0]['districtName']
                    else:
                        b = json_data1['bidpBidLocationList'][0]['districtName'] + ", " + \
                            json_data1['bidpBidLocationList'][0]['provName']

        elif data.find('lsBidpBidLocationDTO') != -1:
            if json_data1['lsBidpBidLocationDTO'] is None:
                b = 0
            else:
                if json_data1['lsBidpBidLocationDTO'][0] is not None:
                    if json_data1['lsBidpBidLocationDTO'][0]['districtName'] is None:
                        b = json_data1['lsBidpBidLocationDTO'][0]['provName']
                    elif json_data1['lsBidpBidLocationDTO'][0]['provName'] is None:
                        b = json_data1['lsBidpBidLocationDTO'][0]['districtName']
                    else:
                        b = json_data1['lsBidpBidLocationDTO'][0]['districtName'] + ", " + \
                            json_data1['lsBidpBidLocationDTO'][0]['provName']

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
        x = str(review1['bidValidityPeriod']) + str(review1['bidValidityPeriodUnit'])

        if review1['guaranteeValue'] is None:
            review1['guaranteeValue'] = 0

        if review1['guaranteeForm'] is None:
            review1['guaranteeForm'] = 0

        if json_data1['bidInvContractorOfflineDTO'] is not None:
            if json_data1['bidInvContractorOfflineDTO']['decisionNo'] is None:
                decisionNo = 0
            else:
                decisionNo = json_data1['bidInvContractorOfflineDTO']['decisionNo']

            if json_data1['bidInvContractorOfflineDTO']['decisionDate'] is None:
                decisionDate = 0
            else:
                decisionDate = json_data1['bidInvContractorOfflineDTO']['decisionDate']

            if json_data1['bidInvContractorOfflineDTO']['decisionAgency'] is None:
                decisionAgency = 0
            else:
                decisionAgency = json_data1['bidInvContractorOfflineDTO']['decisionAgency']

            if json_data1['bidInvContractorOfflineDTO']['decisionFileId'] is not None:
                link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + \
                        json_data1['bidInvContractorOfflineDTO']['decisionFileId'],
            else:
                link1 = 0
        else:
            decisionNo = 0
            decisionDate = 0
            decisionAgency = 0
            link1 = 0

        if review1['id'] is not None:
            link2 = 'https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=' + review1['id'],
        else:
            link2 = 0
        if review1['bidPrice'] is None:
            review1['bidPrice'] = 0

        details.extend(
            [review1['notifyNo'], review1['publicDate'], review1['planNo'], review1['planType'], review1['planName'],
             review1['bidName'], review1['investorName'], review1['procuringEntityName'], review1['capitalDetail'],
             review1['investField'], review1['bidForm'], v, review1['isDomestic'], review1['bidMode'], a,
             review1['isInternet'], review1['issueLocation'], fee, review1['receiveLocation'], b,
             review1['bidCloseDate'], review1['bidOpenDate'], review1['bidOpenLocation'], x, review1['guaranteeValue'],
             review1['guaranteeForm'], decisionNo, decisionDate, decisionAgency, link1, link2, codes])
        with open('' + folder_path1 + '/DHT.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(details)
        details.clear()

    except requests.ReadTimeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so DHT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except requests.exceptions.ConnectionError:
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so DHT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()

        pass

    except requests.Timeout as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so DHT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        f = open('' + folder_path1 + "/log.txt", "a")
        h = "{}".format(code)
        f.write("Ho so DHT bi loi khong lay duoc du lieu: " + h)
        f.write('\n')
        f.close()
        i = random.randrange(1, 10)
        time.sleep(i)
        session1.close()
        session1 = requests.Session()
        details.clear()
        pass

    return


# def CrawlDetail_DT_KCNTTT(code, details, session1, codes, folder_path1, code1, code2):
#     cookies = {
#         'COOKIE_SUPPORT': 'true',
#         'GUEST_LANGUAGE_ID': 'vi_VN',
#         '_ga': 'GA1.1.2001033887.1675655198',
#         'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
#         '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
#         '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
#         '_ga_19996Z37EE': 'deleted',
#         '_ga_19996Z37EE': 'deleted',
#         'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
#         'JSESSIONID': 'P8qD1trpOCbKugcHzLUSfc-EJmmDFcU45yMx_Oyr.dc_app1_02',
#         'LFR_SESSION_STATE_20103': '1677295548357',
#         '_ga_19996Z37EE': 'GS1.1.1677292879.41.1.1677295564.0.0.0',
#         'citrix_ns_id': 'AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==XIP5Yw==yAwzuDLaKsNxiKG6oLupFM7gZGE=',
#     }
#
#     headers = {
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; JSESSIONID=P8qD1trpOCbKugcHzLUSfc-EJmmDFcU45yMx_Oyr.dc_app1_02; LFR_SESSION_STATE_20103=1677295548357; _ga_19996Z37EE=GS1.1.1677292879.41.1.1677295564.0.0.0; citrix_ns_id=AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==XIP5Yw==yAwzuDLaKsNxiKG6oLupFM7gZGE=',
#         'Origin': 'https://muasamcong.mpi.gov.vn',
#         'Pragma': 'no-cache',
#         'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=IB2300026250&notifyId=IB2300026250&inputResultId=b8b48175-5c43-44b2-8590-2ca48a15db5f&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=undefined&notifyNo=IB2300026250&planNo=undefined&pno=undefined',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
#         'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#
#     try:
#         dem = 0
#         nhap1 = [0]
#         nhap1.clear()
#         bien = 0
#         nhap1, bien, dem = CrawDetail_DT_KCNTTT_1(notifyNo=code1, session1=session1, folder_path1=folder_path1, dem=dem)
#
#         nhap2 = [0]
#         nhap2.clear()
#         nhap2 = CrawDetail_DT_KCNTTT_2(inputResultId=code2, session1=session1, folder_path1=folder_path1, nhap2=nhap2)
#         # Request theo id trong list_TBMT_CDT de lay cac thong tin cho vao CT_TBMT_CDT
#         i = random.randrange(1,10)
#         time.sleep(i)
#         session = session1
#         data = '{"id":"' + code + '"}'
#         response = session.post(
#             'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/lcnt/bid-po-bido-notify-contractor-view/get-by-id',
#             cookies=cookies,
#             headers=headers,
#             data=data,
#             allow_redirects=False,
#             verify=False,
#             timeout=30,
#         )
#
#         json_data1 = response.json()
#         if json_data1 is not None:
#             data = json.dumps(json_data1)
#             if data.find('bidoNotifyContractorP') != -1:
#                 if json_data1['bidoNotifyContractorP'] is not None:
#                     review1 = json_data1['bidoNotifyContractorP']
#                     if review1['cPeriod'] is None:
#                         review1['cPeriod'] = 0
#                     if review1['cPeriodUnit'] is None:
#                         review1['cPeriodUnit'] = 0
#                     a = str(review1['cPeriod']) + str(review1['cPeriodUnit'])
#                     if review1['cType'] is not None:
#                         v = review1['cType']
#                     else:
#                         v = 0
#
#             elif data.find('bidoNotifyContractorM') != -1:
#                 if json_data1['bidoNotifyContractorM'] is not None:
#                     review1 = json_data1['bidoNotifyContractorM']
#                     if review1['contractPeriod'] is None:
#                         review1['contractPeriod'] = 0
#                     if review1['contractPeriodUnit'] is None:
#                         review1['contractPeriodUnit'] = 0
#                     a = str(review1['contractPeriod']) + str(review1['contractPeriodUnit'])
#                     if review1['contractType'] is not None:
#                         v = review1['contractType']
#                     else:
#                         v = 0
#
#         if data.find('bidpBidLocationList') != -1:
#             if json_data1['bidpBidLocationList'] is None:
#                 b = 0
#             else:
#                 if json_data1['bidpBidLocationList'][0] is not None:
#                     if json_data1['bidpBidLocationList'][0]['districtName'] is None:
#                         b = json_data1['bidpBidLocationList'][0]['provName']
#                     elif json_data1['bidpBidLocationList'][0]['provName'] is None:
#                         b = json_data1['bidpBidLocationList'][0]['districtName']
#                     else:
#                         b = json_data1['bidpBidLocationList'][0]['districtName'] + ", " + \
#                             json_data1['bidpBidLocationList'][0]['provName']
#
#         elif data.find('lsBidpBidLocationDTO') != -1:
#             if json_data1['lsBidpBidLocationDTO'] is None:
#                 b = 0
#             else:
#                 if json_data1['lsBidpBidLocationDTO'][0] is not None:
#                     if json_data1['lsBidpBidLocationDTO'][0]['districtName'] is None:
#                         b = json_data1['lsBidpBidLocationDTO'][0]['provName']
#                     elif json_data1['lsBidpBidLocationDTO'][0]['provName'] is None:
#                         b = json_data1['lsBidpBidLocationDTO'][0]['districtName']
#                     else:
#                         b = json_data1['lsBidpBidLocationDTO'][0]['districtName'] + ", " + \
#                             json_data1['lsBidpBidLocationDTO'][0]['provName']
#
#         if review1['isInternet'] is None:
#             review1['isInternet'] = 0
#             fee = ''
#         else:
#             if review1['isInternet'] == 1:
#                 if review1['bidForm'] == 'DTRR' or review1['bidForm'] == 'DTHC' or review1['bidForm'] == 'MSTT':
#                     fee = '330,000 VND'
#                 elif review1['bidForm'] == 'CHCT' or review1['bidForm'] == 'CHCTRG':
#                     fee = '220,000 VND'
#             elif review1['isInternet'] == 0:
#                 if review1['feeValue'] is None:
#                     fee = 'Miễn phí'
#                 else:
#                     fee = review1['feeValue']
#
#         if review1['notifyNo'] is None:
#             review1['notifyNo'] = 0
#
#         if review1['publicDate'] is None:
#             review1['publicDate'] = 0
#
#         if review1['planNo'] is None:
#             review1['planNo'] = 0
#
#         if review1['planType'] is None:
#             review1['planType'] = 0
#         else:
#             if review1['planType'] == 'DTPT':
#                 review1['planType'] = 'Chi đầu tư phát triển'
#             elif review1['planType'] == 'TX':
#                 review1['planType'] = 'Chi thường xuyên'
#
#
#         if review1['planName'] is None:
#             review1['planName'] = 0
#
#         if review1['bidName'] is None:
#             review1['bidName'] = 0
#
#         if review1['investorName'] is None:
#             review1['investorName'] = 0
#
#         if review1['procuringEntityName'] is None:
#             review1['procuringEntityName'] = 0
#
#         if review1['capitalDetail'] is None:
#             review1['capitalDetail'] = 0
#
#         if review1['investField'] is None:
#             review1['investField'] = ''
#         else:
#             if review1['investField'] == 'XL':
#                 review1['investField'] = 'Xây lắp'
#             elif review1['investField'] == 'TV':
#                 review1['investField'] = 'Tư vấn'
#             elif review1['investField'] == 'PTV':
#                 review1['investField'] = 'Phi tư vấn'
#             elif review1['investField'] == 'HH':
#                 review1['investField'] = 'Hàng hóa'
#
#         if review1['bidForm'] is None:
#             review1['bidForm'] = 0
#         else:
#             if review1['bidForm'] == 'CHCT':
#                 review1['bidForm'] = 'Chào hàng cạnh tranh'
#             if review1['bidForm'] == 'DTRR':
#                 review1['bidForm'] = 'Đấu thầu rộng rãi'
#             if review1['bidForm'] == 'CHCTRG':
#                 review1['bidForm'] = 'Chào hàng cạnh tranh rút gọn'
#             if review1['bidForm'] == 'CDTRG':
#                 review1['bidForm'] = 'Chỉ định thầu rút gọn'
#
#         if review1['isDomestic'] is None:
#             review1['isDomestic'] = 0
#         else:
#             if review1['isDomestic'] == 1:
#                 review1['isDomestic'] = 'Trong nước'
#             elif review1['isDomestic'] == 0:
#                 review1['isDomestic'] = 'Quốc tế'
#
#         if review1['bidMode'] is None:
#             review1['bidMode'] = 0
#         else:
#             if review1['bidMode'] == '1_MTHS':
#                 review1['bidMode'] = 'Một giai đoạn một túi hồ sơ'
#             elif review1['bidMode'] == '1_HTHS':
#                 review1['bidMode'] = 'Một giai đoạn hai túi hồ sơ'
#
#         if review1['isInternet'] is None:
#             review1['isInternet'] = 0
#         else:
#             if review1['isInternet'] == 1:
#                 review1['isInternet'] = 'Qua mạng'
#             elif review1['isInternet'] == 0:
#                 review1['isInternet'] = 'Không qua mạng'
#
#         if review1['issueLocation'] is None:
#             review1['issueLocation'] = 0
#
#         if review1['receiveLocation'] is None:
#             review1['receiveLocation'] = 0
#
#         if review1['bidCloseDate'] is None:
#             review1['bidCloseDate'] = 0
#
#         if review1['bidOpenDate'] is None:
#             review1['bidOpenDate'] = 0
#
#         if review1['bidOpenLocation'] is None:
#             review1['bidOpenLocation'] = 0
#
#         if review1['bidValidityPeriod'] is None:
#             review1['bidValidityPeriod'] = 0
#
#         if review1['bidValidityPeriodUnit'] is None:
#             review1['bidValidityPeriodUnit'] = 0
#
#         if review1['guaranteeValue'] is None:
#             review1['guaranteeValue'] = 0
#
#         if review1['guaranteeForm'] is None:
#             review1['guaranteeForm'] = 0
#
#         if json_data1['bidInvContractorOfflineDTO'] is not None:
#             if json_data1['bidInvContractorOfflineDTO']['decisionNo'] is None:
#                 decisionNo = 0
#             else:
#                 decisionNo = json_data1['bidInvContractorOfflineDTO']['decisionNo']
#
#             if json_data1['bidInvContractorOfflineDTO']['decisionDate'] is None:
#                 decisionDate = 0
#             else:
#                 decisionDate = json_data1['bidInvContractorOfflineDTO']['decisionDate']
#
#             if json_data1['bidInvContractorOfflineDTO']['decisionAgency'] is None:
#                 decisionAgency = 0
#             else:
#                 decisionAgency = json_data1['bidInvContractorOfflineDTO']['decisionAgency']
#
#             if json_data1['bidInvContractorOfflineDTO']['decisionFileId'] is not None:
#                 link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + \
#                         json_data1['bidInvContractorOfflineDTO']['decisionFileId'],
#             else:
#                 link1 = 0
#         else:
#             decisionNo = 0
#             decisionDate = 0
#             decisionAgency = 0
#             link1 = 0
#
#         if review1['id'] is not None:
#             link2 = 'https://muasamcong.mpi.gov.vn/egp/contractorfe/viewer?formCode=ALL&id=' + review1['id'],
#         else:
#             link2 = 0
#         if review1['bidPrice'] is None:
#             review1['bidPrice'] = 0
#
#         if review1["notifyVersion"] is None:
#             review1["notifyVersion"] = ''
#
#         details.extend([review1['notifyNo'],
#                         review1['publicDate'],
#                         review1["notifyVersion"],
#                         review1['planNo'],
#                         review1['planType'],
#                         review1['planName'],
#                         review1['bidName'],
#                         review1['investorName'],
#                         review1['procuringEntityName'],
#                         review1['capitalDetail'],
#                         review1['investField'],
#                         review1['bidForm'],
#                         v,
#                         review1['isDomestic'],
#                         review1['bidMode'],
#                         a,
#                         review1['isInternet'],
#                         review1['issueLocation'],
#                         fee,
#                         review1['receiveLocation'],
#                         b,
#                         review1['bidCloseDate'],
#                         review1['bidOpenDate'],
#                         review1['bidOpenLocation'],
#                         str(review1['bidValidityPeriod']) + str(review1['bidValidityPeriodUnit']),
#                         review1['guaranteeValue'],
#                         review1['bidPrice'],
#                         review1['guaranteeForm'],
#                         decisionNo,
#                         decisionDate,
#                         decisionAgency,
#                         link1,
#                         link2,
#                         dem,
#                         bien,
#                         nhap1,
#                         nhap2,
#                         codes])
#         bidType = upABN_db.bid_type(details[10])
#         bidMethod = upABN_db.bid_method(details[16])
#         crea_at = upABN_db.timeUpd()
#         tim_close = upABN_db.time_close(details[21])
#         time_post = upABN_db.time_post(details[1])
#         date_app = upABN_db.date_app2(decisionDate)
#         news_id = 0
#         print('1111')
#         if upABN_db.ktTrungDL(review1['notifyNo'], review1["notifyVersion"]) == None:
#             news_id = upABN_db.upDataDB(8, bidType, bidMethod, 1, crea_at, crea_at, review1['notifyNo'],
#                                         review1["notifyVersion"],
#                                         tim_close, time_post, date_app)
#             print('news_kcnttt')
#             upABO_result_complete_gd_hsdt.upData(details, news_id, 0)
#             print(2)
#
#
#         with open('' + folder_path1 + '/CNTTT.csv', 'a', encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow(details)
#         details.clear()
#
#
#     except requests.ReadTimeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(code)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.exceptions.ConnectionError:
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(code)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.Timeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(code)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except Exception as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(code)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#     return
#
#
# def CrawDetail_DT_KCNTTT_KQM(inputResultId, details, session1, codes, folder_path1):
#     cookies = {
#         'COOKIE_SUPPORT': 'true',
#         'GUEST_LANGUAGE_ID': 'vi_VN',
#         '_ga': 'GA1.1.2001033887.1675655198',
#         'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
#         '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
#         '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
#         '_ga_19996Z37EE': 'deleted',
#         '_ga_19996Z37EE': 'deleted',
#         'JSESSIONID': 'EjKa8X-ItOKYz3qrc56vTR8hRaJnyjC3AtCO45_o.dc_app1_01',
#         'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
#         'LFR_SESSION_STATE_20103': '1677296447665',
#         '_ga_19996Z37EE': 'GS1.1.1677292879.41.1.1677296463.0.0.0',
#         'citrix_ns_id': 'AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==3ob5Yw==lBkRIhhcwjXAP8AyH8OfnzTA8ow=',
#     }
#
#     headers = {
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=EjKa8X-ItOKYz3qrc56vTR8hRaJnyjC3AtCO45_o.dc_app1_01; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; LFR_SESSION_STATE_20103=1677296447665; _ga_19996Z37EE=GS1.1.1677292879.41.1.1677296463.0.0.0; citrix_ns_id=AAE7TXX5YztZ3bkAAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==3ob5Yw==lBkRIhhcwjXAP8AyH8OfnzTA8ow=',
#         'Origin': 'https://muasamcong.mpi.gov.vn',
#         'Pragma': 'no-cache',
#         'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=IB2300024175&notifyId=IB2300024175&inputResultId=2aad6a2a-cff4-43a8-8a8e-93c576c05867&bidOpenId=undefined&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=undefined&notifyNo=IB2300024175&planNo=undefined&pno=undefined',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
#         'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     try:
#         i = random.randrange(1,10)
#         time.sleep(i)
#         session = session1
#         data = '{"id":"' + inputResultId + '"}'
#         response = session.post(
#             'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/contractor-input-result/get',
#             cookies=cookies,
#             headers=headers,
#             data=data,
#             allow_redirects=False,
#             verify=False,
#             timeout=30,
#         )
#         json_data1 = response.json()
#         if json_data1 is None:
#             return
#         else:
#             if json_data1['bideContractorInputResultDTO'] is not None:
#                 review1 = json_data1['bideContractorInputResultDTO']
#             if json_data1['bidpPlanDetailDTO'] is not None:
#                 review2 = json_data1['bidpPlanDetailDTO']
#
#         if review1['notifyNo'] is None:
#             review1['notifyNo'] = 0
#
#         if review1['publicDate'] is None:
#             review1['publicDate'] = 0
#
#         if review1['investorName'] is None:
#             review1['investorName'] = 0
#
#         if review2['planNo'] is None:
#             review2['planNo'] = 0
#
#         if review1['bidName'] is None:
#             review1['bidName'] = 0
#
#         if review1['bidEstimatePrice'] is None:
#             review1['bidEstimatePrice'] = 0
#
#         if review1['bidPrice'] is None:
#             review1['bidPrice'] = 0
#
#         if review1['ctype'] is None:
#             review1['ctype'] = 0
#
#         if review1['bidForm'] is None:
#             review1['bidForm'] = 0
#
#         if review1['bidMode'] is None:
#             review1['bidMode'] = 0
#
#         if review1['bidField'] is None:
#             review1['bidField'] = 0
#
#         if review1['decisionDate'] is None:
#             review1['decisionDate'] = 0
#
#         if review1['decisionAgency'] is None:
#             review1['decisionAgency'] = 0
#
#         if review1['decisionNo'] is None:
#             review1['decisionNo'] = 0
#
#         if review1['reportFileId'] is None:
#             link1 = 0
#         else:
#             link1 = 'http://localhost:1234/api/download/file/browser/public?fileId=' + review1['reportFileId']
#
#         if review1['isDomestic'] is None:
#             review1['isDomestic'] = ''
#         else:
#             if review1['isDomestic'] == 1 or review1['isDomestic'] == True:
#                 review1['isDomestic'] = 'Trong nước'
#             else:
#                 review1['isDomestic'] = 'Quốc tế'
#
#         nhap = [0]
#         nhap.clear()
#         if review1['lotResultDTO'] is not None:
#             if review1['lotResultDTO'][0] is not None:
#                 if review1['lotResultDTO'][0]['contractorList'] is not None:
#                     for nhathau in review1['lotResultDTO'][0]['contractorList']:
#                         if nhathau['bidResult'] == 1:
#                             if nhathau['orgCode'] is None:
#                                 nhathau['orgCode'] = 0
#
#                             if nhathau['orgFullname'] is None:
#                                 nhathau['orgFullname'] = 0
#
#                             if nhathau['bidWiningPrice'] is None:
#                                 nhathau['bidWiningPrice'] = 0
#
#                                 nhap.append([nhathau['orgCode'], nhathau['orgFullname'], nhathau['bidWiningPrice']])
#
#         details.extend(
#             [review1['notifyNo'], review1['publicDate'], review1['investorName'], review2['planNo'], review1['bidName'],
#              review1['bidEstimatePrice'], review1['bidPrice'], review1['ctype'], review1['bidForm'], review1['bidMode'],
#              review1['bidField'], review1['decisionDate'], review1['decisionAgency'], review1['decisionNo'], link1,
#              review1['isDomestic'], nhap, codes])
#         with open('' + folder_path1 + '/CNTTT_KQM.csv', 'a', encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow(details)
#         details.clear()
#
#
#     except requests.ReadTimeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.exceptions.ConnectionError:
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.Timeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except Exception as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so CNTTT KQM bi loi khong lay duoc du lieu: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#     return
#
#
# def CrawDetail_DT_KCNTTT_1(notifyNo, session1, folder_path1, dem):
#     cookies2 = {
#         'COOKIE_SUPPORT': 'true',
#         'GUEST_LANGUAGE_ID': 'vi_VN',
#         '_ga': 'GA1.1.2001033887.1675655198',
#         'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
#         '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
#         '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
#         '_ga_19996Z37EE': 'deleted',
#         '_ga_19996Z37EE': 'deleted',
#         'JSESSIONID': '2M0FtYPE249N-JxE30p-BxDAclmuUln5yBJKNNIQ.dc_app1_01',
#         'LFR_SESSION_STATE_20103': '1676788514796',
#         'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2345525d5f4f58455e445a4a4217de',
#         '_ga_19996Z37EE': 'GS1.1.1676788070.5.1.1676789211.0.0.0',
#         'citrix_ns_id': 'AAE7ar_xYzvrK64AAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==YsnxYw==x_2EGEljGY2abWHfUM_y5bDiYlY=',
#     }
#
#     headers2 = {
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; JSESSIONID=2M0FtYPE249N-JxE30p-BxDAclmuUln5yBJKNNIQ.dc_app1_01; LFR_SESSION_STATE_20103=1676788514796; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2345525d5f4f58455e445a4a4217de; _ga_19996Z37EE=GS1.1.1676788070.5.1.1676789211.0.0.0; citrix_ns_id=AAE7ar_xYzvrK64AAAAAADuFeyfrzB16Q6f2OzBmufpqrxJznGrtoFWvkMWyR9BuOw==YsnxYw==x_2EGEljGY2abWHfUM_y5bDiYlY=',
#         'Origin': 'https://muasamcong.mpi.gov.vn',
#         'Pragma': 'no-cache',
#         'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=8051e056-f3b3-4318-bf09-baa91ee3d95d&notifyId=8051e056-f3b3-4318-bf09-baa91ee3d95d&inputResultId=eaf045bc-91fe-4e5d-a02e-fea93bb1bb90&bidOpenId=eafe7066-9c56-4db7-a642-42e7c4674d11&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300018722&planNo=PL2300014693&pno=undefined',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0',
#         'sec-ch-ua': '"Chromium";v="108", "Opera GX";v="94", "Not)A;Brand";v="99"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     try:
#         i = random.randrange(1,10)
#         time.sleep(i)
#         session = session1
#         data2 = '{"notifyNo":"' + notifyNo + '","type":"TBMT","packType":0}'
#         response2 = session.post(
#             'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/ldtkqmt/bid-notification-p/get-by-id',
#             cookies=cookies2,
#             headers=headers2,
#             data=data2,
#             allow_redirects=False,
#             verify=False,
#             timeout=30,
#         )
#
#         json_data2 = response2.json()
#         review2 = json_data2
#         nhap1 = [0]
#         nhap1.clear()
#         if review2 is None:
#             return 0, 0, 0
#         else:
#             if review2['bidSubmissionByContractorViewResponse'] is None:
#                 return 0, 0, 0
#             else:
#                 if review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList'] is None:
#                     return 0, 0, 0
#                 if review2['bidoBidroundMngViewDTO']['successBidOpenDate'] is None:
#                     review2['bidoBidroundMngViewDTO']['successBidOpenDate'] = 0
#
#         for nhathau in review2['bidSubmissionByContractorViewResponse']['bidSubmissionDTOList']:
#             if nhathau['contractorCode'] is None:
#                 nhathau['contractorCode'] = 0
#
#             if nhathau['contractorName'] is None:
#                 nhathau['contractorName'] = 0
#
#             if nhathau['bidPrice'] is None:
#                 nhathau['bidPrice'] = 0
#
#             if nhathau['alternativeTech'] is None:
#                 nhathau['alternativeTech'] = 0
#
#             if nhathau['bidFinalPrice'] is None:
#                 nhathau['bidFinalPrice'] = 0
#
#             if nhathau['bidValidityNum'] is None:
#                 nhathau['bidValidityNum'] = 0
#
#             if nhathau['bidGuarantee'] is None:
#                 nhathau['bidGuarantee'] = 0
#
#             if nhathau['bidGuaranteeValidity'] is None:
#                 nhathau['bidGuaranteeValidity'] = 0
#
#             if nhathau['contractPeriodDT'] is None:
#                 nhathau['contractPeriodDT'] = 0
#
#             if nhathau['contractPeriodDTUnit'] is None:
#                 nhathau['contractPeriodDTUnit'] = 0
#
#             nhap1.append(
#                 [nhathau['contractorCode'], nhathau['contractorName'], nhathau['bidPrice'], nhathau['alternativeTech'],
#                  nhathau['bidFinalPrice'], nhathau['bidValidityNum'], nhathau['bidGuarantee'],
#                  nhathau['bidGuaranteeValidity'],
#                  str(nhathau['contractPeriodDT']) + str(nhathau['contractPeriodDTUnit'])])
#             dem = dem + 1
#
#         return nhap1, review2['bidoBidroundMngViewDTO']['successBidOpenDate'], dem
#
#
#     except requests.ReadTimeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(notifyNo)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.exceptions.ConnectionError:
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(notifyNo)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.Timeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(notifyNo)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except Exception as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(notifyNo)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 3: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#
# def CrawDetail_DT_KCNTTT_2(inputResultId, session1, folder_path1, nhap2):
#     cookies3 = {
#         'COOKIE_SUPPORT': 'true',
#         'GUEST_LANGUAGE_ID': 'vi_VN',
#         '_ga': 'GA1.1.2001033887.1675655198',
#         'df5f782085f475fb47cf8ea13597bc51': 'b4ea14c8fd0889330ffb706942522708',
#         '40e12b6a56cf7542c4f2bdc7816f154a': 'e9b4751a7a0ab8ff3c186dc483234702',
#         '5321a273c51a75133e0fb1cd75e32e27': 'ade5164d2e0fd8c83bfac03e189c2b3a',
#         '_ga_19996Z37EE': 'deleted',
#         '_ga_19996Z37EE': 'deleted',
#         'LFR_SESSION_STATE_20103': '1677299771614',
#         'NSC_WT_QSE_QPSUBM_NTD_NQJ': 'ffffffffaf183e2245525d5f4f58455e445a4a4217de',
#         'JSESSIONID': 'j32Jyt6aLSDjzUCPbJ54aLZszP5dzJwMXAj-_n7i.dc_app1_02',
#         '_ga_19996Z37EE': 'GS1.1.1677302324.43.1.1677302340.0.0.0',
#         'citrix_ns_id': 'AAQ7MZr5YzucIbwAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==y535Yw==exYEMKTSv390EFm78JcEbK4CM14=',
#     }
#
#     headers3 = {
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Content-Type': 'application/json',
#         # 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=vi_VN; _ga=GA1.1.2001033887.1675655198; df5f782085f475fb47cf8ea13597bc51=b4ea14c8fd0889330ffb706942522708; 40e12b6a56cf7542c4f2bdc7816f154a=e9b4751a7a0ab8ff3c186dc483234702; 5321a273c51a75133e0fb1cd75e32e27=ade5164d2e0fd8c83bfac03e189c2b3a; _ga_19996Z37EE=deleted; _ga_19996Z37EE=deleted; LFR_SESSION_STATE_20103=1677299771614; NSC_WT_QSE_QPSUBM_NTD_NQJ=ffffffffaf183e2245525d5f4f58455e445a4a4217de; JSESSIONID=j32Jyt6aLSDjzUCPbJ54aLZszP5dzJwMXAj-_n7i.dc_app1_02; _ga_19996Z37EE=GS1.1.1677302324.43.1.1677302340.0.0.0; citrix_ns_id=AAQ7MZr5YzucIbwAAAAAADuFeyfrzB16Q6f2O8qetWxEjgrmsRagqTk7pAb08kWUOw==y535Yw==exYEMKTSv390EFm78JcEbK4CM14=',
#         'Origin': 'https://muasamcong.mpi.gov.vn',
#         'Pragma': 'no-cache',
#         'Referer': 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?p_p_id=egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_egpportalcontractorselectionv2_WAR_egpportalcontractorselectionv2_render=detail&type=es-notify-contractor&stepCode=notify-contractor-step-4-kqlcnt&id=aca05bb6-40b7-43a7-b4f8-9fcb5ddb9097&notifyId=aca05bb6-40b7-43a7-b4f8-9fcb5ddb9097&inputResultId=a313cf55-5bc5-4003-9cb4-8fde3e4dc2ad&bidOpenId=00e4e371-cb82-4d7a-8cca-b432cceb9580&techReqId=undefined&bidPreNotifyResultId=undefined&bidPreOpenId=undefined&processApply=LDT&bidMode=1_MTHS&notifyNo=IB2300023119&planNo=PL2300018300&pno=undefined',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0',
#         'sec-ch-ua': '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#     }
#     try:
#         i = random.randrange(1,10)
#         time.sleep(i)
#         session = session1
#         data3 = '{"id":"' + inputResultId + '"}'
#         response3 = session.post(
#             'https://muasamcong.mpi.gov.vn/o/egp-portal-contractor-selection-v2/services/expose/contractor-input-result/get',
#             cookies=cookies3,
#             headers=headers3,
#             data=data3,
#             allow_redirects=False,
#             verify=False,
#             timeout=30,
#         )
#
#         json_data3 = response3.json()
#         review3 = json_data3
#         nhap2 = [0]
#         nhap2.clear()
#         if review3 is None:
#             return
#         else:
#             if review3['bideContractorInputResultDTO'] is None:
#                 return
#             else:
#                 if review3['bideContractorInputResultDTO']['lotResultDTO'] is None:
#                     return
#                 else:
#                     if review3['bideContractorInputResultDTO']['lotResultDTO'][0] is None:
#                         return
#                     else:
#                         if review3['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList'] is None:
#                             return
#
#         for nhathau in review3['bideContractorInputResultDTO']['lotResultDTO'][0]['contractorList']:
#             if nhathau['orgCode'] is None:
#                 nhathau['orgCode'] = 0
#
#             if nhathau['orgFullname'] is None:
#                 nhathau['orgCode'] = 0
#
#             if nhathau['lotFinalPrice'] is None:
#                 nhathau['orgCode'] = 0
#
#             if nhathau['bidWiningPrice'] is None:
#                 nhathau['orgCode'] = 0
#
#             if nhathau['cperiod'] is None:
#                 nhathau['orgCode'] = 0
#
#             if nhathau['cperiodUnit'] is None:
#                 nhathau['orgCode'] = 0
#
#             if nhathau['bidResult'] is None:
#                 nhap2.append([nhathau['orgCode'], nhathau['orgFullname'], nhathau['reason'], 0, 0])
#
#             elif nhathau['bidResult'] == 1:
#                 nhap2.append(
#                     [nhathau['orgCode'], nhathau['orgFullname'], nhathau['lotFinalPrice'], nhathau['bidWiningPrice'],
#                      str(nhathau['cperiod']) + nhathau['cperiodUnit']])
#
#         return nhap2
#     except requests.ReadTimeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.exceptions.ConnectionError:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except requests.Timeout as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass
#
#     except Exception as err:
#         print(f"{type(err).__name__} was raised: {err}")
#         f = open('' + folder_path1 + "/log.txt", "a")
#         h = "{}".format(inputResultId)
#         f.write("Ho so TBMT CNTTT bi loi khong lay duoc du lieu 2: " + h)
#         f.write('\n')
#         f.close()
#         i = random.randrange(1, 10)
#         time.sleep(i)
#         session1.close()
#         session1 = requests.Session()
#         pass


SoTrangNT = SoTrangNhaThau(startDay, endDay)
SoTrangBMT = SoTrangBenMoiThau(startDay, endDay)
SoTrangTT = SoTrangTinTuc(startDay, endDay)
SoTrangDT = SoTrangTinTucDongThau(startDay, endDay)

# main
try:

    folder_path = './' + startDay + 'to' + endDay + ''

    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    thread_TinTuc = 15
    # DA
    # KHLCNT
    # TBMT CDT

    thread_NhaThau = 2

    thread_BenMoiThau = 2

    thread_TinTucDongThau = 15

    thread_upData = 1

    thread_changeData = 0

    totalThread = thread_upData + thread_BenMoiThau + thread_TinTuc + thread_NhaThau + thread_TinTucDongThau

    threads = []
    dem_TT = 0
    dem_NT = 0
    dem_BMT = 0
    dem_DT = 0
    dem_upData = 0
    time_start = datetime.now()

    for i in range(totalThread):
        a = i + 1
        b = str(a)
        if i <= thread_TinTuc - 1:
            thread = MyThread(i, "thread" + b, thread_TinTuc, 'TT', dem_TT, thread_TinTuc)
            dem_TT = dem_TT + 1

        elif i > thread_TinTuc - 1 and i <= thread_TinTuc + thread_NhaThau - 1:
            thread = MyThread(i, "thread" + b, thread_NhaThau, 'NT', dem_NT, thread_NhaThau)
            dem_NT = dem_NT + 1

        elif i > thread_TinTuc + thread_NhaThau - 1 and i <= thread_BenMoiThau + thread_TinTuc + thread_NhaThau - 1:
            thread = MyThread(i, "thread" + b, thread_BenMoiThau, 'BMT', dem_BMT, thread_BenMoiThau)
            dem_BMT = dem_BMT + 1

        elif (i > thread_BenMoiThau + thread_TinTuc + thread_NhaThau - 1) and (
                i <= thread_BenMoiThau + thread_TinTuc + thread_NhaThau + thread_TinTucDongThau - 1):
            thread = MyThread(i, "thread" + b, thread_TinTucDongThau, 'DT', dem_DT, thread_TinTucDongThau)
            dem_DT = dem_DT + 1

        elif i > thread_BenMoiThau + thread_TinTuc + thread_NhaThau + thread_TinTucDongThau - 1 and i <= totalThread - 1:
            thread = MyThread(i, "thread" + b, thread_upData, 'upData', dem_upData, thread_upData)
            dem_upData = dem_upData + 1
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

except Exception as err:
    print(f"{type(err).__name__} was raised: {err}")
    f = open('' + folder_path + "/log.txt", "a")
    f.write("Chuong trinh bi loi")
    f.write('\n')
    f.close()

