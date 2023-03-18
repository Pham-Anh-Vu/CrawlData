import ftplib
import os
import urllib.request

def downFileAndUpLoad(url,file_name):
    # URL of the file to download

    url = 'http://localhost:1234/api/download/file/browser/public?fileId=228c5a9c-7886-4bdb-9b7a-3756f9012fe9'
    file_name = '2023218163243430_2.1.+CHƯƠNG+V+YÊU+CẦU+VỀ+KỸ+THUẬT+GÓI+THẦU+XL-05+.pdf'
    # Download the file
    urllib.request.urlretrieve(url, './download/'+file_name)

    # Wait until the download finishes
    urllib.request.urlcleanup()

    # Set the FTP server details
    ftp_server = 'ctd.com.vn'
    ftp_username = 'test@ctd.com.vn'
    ftp_password = 'Nmd021200.'

    local_file_path = './download/'+file_name
    remote_file_path = '/muasamcong/thongbaomoithau/'
    remote_file_path_name = remote_file_path + file_name
    # Open the FTP connection
    with ftplib.FTP(ftp_server) as ftp:
        # Log in to the FTP server
        ftp.login(user=ftp_username, passwd=ftp_password)
        ftp.cwd(remote_file_path)
            # Check if the remote file exists
        if file_name in ftp.nlst():
            # If the remote file exists, generate a new filename
            i = 1
            while True:
                new_file_name = '{}_{}{}'.format(os.path.splitext(file_name)[0], i, os.path.splitext(file_name)[1])
                if new_file_name not in ftp.nlst():
                    new_file_path = remote_file_path + new_file_name
                    file_name = new_file_name
                    remote_file_path_name = new_file_path
                    break
                i += 1

        # Open the local file
        with open(local_file_path, 'rb') as f:
            # Upload the file to the server
            ftp.storbinary('STOR {}'.format(os.path.basename(file_name)), f)
        type = os.path.splitext(file_name)[1].replace('.','')
        name = file_name
        path = remote_file_path_name
    return name,type,path