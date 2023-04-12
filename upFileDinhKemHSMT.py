import ftplib
import os
import urllib.request
import cgi
import urllib.parse
from urllib.request import urlopen

from minio import Minio
from minio.error import S3Error


client = Minio(
        "storage.rsa.vn:9000",
        access_key="5nPH7GkDwdE82lGZ",
        secret_key="z2HRBHivdO13OVGYHQ0x1j4J3qbfCspW",
        secure= False
        )

def downFileAndUpLoad(code):
    url = 'http://localhost:1234/api/download/file/browser/public?fileId='+ code
    
    name = ''
    type = ''
    path = ''
    file_name_for_user =''
    try:
        folder_pathz = 'C:\\MPI\\EGP-AGENT\\DOWNLOAD\\'
        if not os.path.isdir(folder_pathz):
            os.mkdir(folder_pathz)
        # URL of the file to download

        remotefile = urlopen(url)
        contentdisposition = remotefile.info()['Content-Disposition']
        _, params = cgi.parse_header(contentdisposition)
        filename = params["filename"]
        file_name = urllib.parse.unquote(filename)
        base, ext= os.path.splitext(file_name)
        # Tạo tên file mới
        file_name = base.replace("+", " ")
        file_name_a = file_name.split("_")[1] + ext
        file_name = file_name.split("_")[0]+'-'+file_name.split("_")[1] + ext
        local_file_path = 'C:\\MPI\\EGP-AGENT\\DOWNLOAD\\'+file_name
        file_name_for_user = file_name
        if os.path.exists(local_file_path):
            # Nếu tên file đã tồn tại, thêm số thứ tự vào sau tên file để đổi tên
            i = 1
            new_filename = file_name
            local_file_path = './download/'+new_filename
            while os.path.exists(local_file_path):
                base, ext = os.path.splitext(file_name)
                new_filename = "{}_{}{}".format(base, i, ext)
                i += 1
                local_file_path = 'C:\\MPI\\EGP-AGENT\\DOWNLOAD\\'+new_filename
            file_name = new_filename
            local_file_path = 'C:\\MPI\\EGP-AGENT\\DOWNLOAD\\'+file_name

        # Wait until the download finishes
        urllib.request.urlcleanup()

        local_file_path = 'C:\\MPI\\EGP-AGENT\\DOWNLOAD\\'+file_name
        remote_file_path = '/muasamcong/thongbaomoithau/'
        remote_file_path_name = remote_file_path + file_name
        
        found = client.bucket_exists("test")
        
        if not found:
            client.make_bucket("test")

        file_name, new_file_name = rename_file_if_exists('test',file_name,0,remote_file_path)

        a = client.put_object(
            "test", '/muasamcong/thongbaomoithau/'+new_file_name, remotefile, length=-1 ,content_type="application/octet-stream", part_size=10*1024*1024
            )

        type = os.path.splitext(file_name_a)[1].replace('.','')
        name = new_file_name
        path = remote_file_path + new_file_name
        file_name_for_user = 'File đính kèm: '+file_name_for_user

        bucket_name = 'test'
        object_name = '/muasamcong/thongbaomoithau/'+new_file_name
        file_path = local_file_path
        object_info = client.stat_object(bucket_name, object_name)
        check = 1

    except S3Error as exc:
        check = 0
        print("error occurred.", exc)
        pass

    except:
        check = 0
        pass
    
    return check,name,type,path, file_name_for_user


def is_object_exists(bucket_name, object_name):
    try:
        client.stat_object(bucket_name, object_name)
        return True
    except S3Error as err:
        # Nếu object không tồn tại
        return False

# Hàm để đổi tên file nếu file đã tồn tại
def rename_file_if_exists(bucket_name, file_name, count,path):
    new_file_name = file_name
    while is_object_exists(bucket_name, (path+new_file_name)):
        # Tách tên file và đuôi file
        name, extension = os.path.splitext(file_name)
        # Thêm số vào tên file
        name = name + '-' + str(count)
        # Ghép lại tên file và đuôi file
        new_file_name = name + extension
        count = count + 1 
    return file_name, new_file_name