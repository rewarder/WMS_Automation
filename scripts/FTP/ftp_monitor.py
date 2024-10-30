import ftplib
import os
import time

# FTP server details
FTP_HOST = 'portal.tedamos.com'
FTP_USER = 'mbtiles'
FTP_PASS = 'mb-layer3311'
FTP_MONITOR_DIR = '/plandata'

# Local directories
LOCAL_DIR = '/home/debian/WMS_Upload/data'
PROCESSED_DIR = '/home/debian/WMS_Upload/data/processed'

def connect_to_ftp():
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    return ftp

def list_files(ftp, path):
    items = []
    ftp.cwd(path)
    ftp.retrlines('MLSD', items.append)
    return items

def download_file(ftp, ftp_path, local_path):
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f'RETR ' + ftp_path, f.write)

def monitor_ftp_directory(ftp):
    known_files = set()

    while True:
        new_files = check_for_new_files(ftp, FTP_MONITOR_DIR, known_files)
        for file in new_files:
            filename = os.path.basename(file)
            processed_path = os.path.join(PROCESSED_DIR, filename)

            # Check if file already exists in the processed directory
            if not os.path.exists(processed_path):
                local_path = os.path.join(LOCAL_DIR, filename)
                download_file(ftp, file, local_path)
                print(f'New file downloaded: {local_path}')
            else:
                print(f'File already exists in processed: {filename}')

        time.sleep(60)  # Check every 60 seconds

def check_for_new_files(ftp, path, known_files):
    new_files = []
    items = list_files(ftp, path)
    
    for item in items:
        parts = item.split(';')
        type_info = [p for p in parts if p.startswith('type=')][0]
        name_info = [p for p in parts if p.startswith(' ')][0].strip()
        entry_type = type_info.split('=')[1]
        name = name_info

        if entry_type == 'file':
            file_path = os.path.join(path, name)
            if file_path not in known_files:
                known_files.add(file_path)
                new_files.append(file_path)
        elif entry_type == 'dir':
            new_files.extend(check_for_new_files(ftp, os.path.join(path, name), known_files))
    
    return new_files

if __name__ == '__main__':
    ftp_connection = connect_to_ftp()
    try:
        monitor_ftp_directory(ftp_connection)
    finally:
        ftp_connection.quit()