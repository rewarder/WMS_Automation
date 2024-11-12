import ftplib
import os
import time
import argparse
from datetime import datetime

# FTP server details
FTP_HOST = 'portal.tedamos.com'
FTP_USER = 'mbtiles'
FTP_PASS = 'mb-layer3311'
FTP_MONITOR_DIR = '/plandata'

# Local directories
LOCAL_DIR = '/home/debian/WMS_Automation/input'
PROCESSED_DIR = '/home/debian/WMS_Automation/processed'
OUTPUT_DIR = '/home/debian/WMS_Automation/output'

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor and download files from an FTP server.')
    parser.add_argument('--cutoff-date', type=str, required=True, help='Cut-off date in YYYY-MM-DD format.')
    args = parser.parse_args()
    return datetime.strptime(args.cutoff_date, '%Y-%m-%d')

def get_file_modification_time(item):
    for part in item.split(';'):
        if part.startswith('modify='):
            mod_time_str = part.split('=')[1]
            return datetime.strptime(mod_time_str, '%Y%m%d%H%M%S')
    return None

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

def monitor_ftp_directory(ftp, cutoff_date):
    known_files = set()

    while True:
        new_files = check_for_new_files(ftp, FTP_MONITOR_DIR, known_files)
        for file in new_files:
            filename = os.path.basename(file)
            file_ext = os.path.splitext(filename)[1].lower()
            
            # Ignore .txt files
            if file_ext == '.txt':
                print(f'Ignoring .txt file: {filename}')
                continue

            # Determine the appropriate directory based on file extension
            if file_ext == '.dxf':
                local_path = os.path.join(LOCAL_DIR, filename)
            elif file_ext in '.json':
                local_path = os.path.join(OUTPUT_DIR, filename)
            else:
                print(f'Unknown file type: {filename}')
                continue
            
            processed_path = os.path.join(PROCESSED_DIR, filename)
            
            # Check file modification time
            items = list_files(ftp, os.path.dirname(file))
            file_item = next((item for item in items if filename in item), None)
            if file_item:
                mod_time = get_file_modification_time(file_item)
                if mod_time and mod_time < cutoff_date:
                    print(f'Skipping file {filename} due to cut-off date')
                    continue

            # Check if file already exists in the processed directory
            if not os.path.exists(processed_path):
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
    cutoff_date = parse_arguments()
    ftp_connection = connect_to_ftp()
    try:
        monitor_ftp_directory(ftp_connection, cutoff_date)
    finally:
        ftp_connection.quit()