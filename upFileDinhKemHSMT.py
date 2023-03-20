import ftplib
import os
import urllib.request
import cgi
import urllib.parse

def downFileAndUpLoad(url):
    folder_pathz = './download'
    if not os.path.isdir(folder_pathz):
        os.mkdir(folder_pathz)
    # URL of the file to download

    remotefile = urllib.request.urlopen(url)
    contentdisposition = remotefile.info()['Content-Disposition']
    _, params = cgi.parse_header(contentdisposition)
    filename = params["filename"]
    file_name = urllib.parse.unquote(filename)
    base, ext= os.path.splitext(file_name)
    # Tạo tên file mới
    file_name = base.replace("+", " ")
    file_name = file_name.split("_")[1] + ext
    local_file_path = './download/'+file_name
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
                local_file_path = './download/'+new_filename
            file_name = new_filename
            local_file_path = './download/'+file_name

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
        file_name_for_user = 'File đính kèm: '+file_name_for_user
    return name,type,path, file_name_for_user