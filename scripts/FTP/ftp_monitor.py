import ftplib
import os
import time

FTP_SERVER = "portal.tedamos.com"
FTP_USER = "mbtiles"
FTP_PASS = "mb-layer3311"
REMOTE_DIR = "/plandata"
LOCAL_DIR = "/home/debian/WMS_Upload/data"

def get_file_list(ftp, remote_dir):
    stack = [remote_dir]
    file_list = []

    while stack:
        current_dir = stack.pop()
        try:
            ftp.cwd(current_dir)  # Change to the current directory
            items = ftp.nlst()  # List items in the current directory

            for item in items:
                item_path = os.path.join(current_dir, item)
                try:
                    ftp.cwd(item_path)  # Try to change into the item (directory)
                    stack.append(item_path)  # If it's a directory, add it to the stack
                except ftplib.error_perm:
                    # If it fails, it's a file; add to the list
                    file_list.append(item_path)

            ftp.cwd('..')  # Go back to the parent directory after processing the current one
        except ftplib.error_perm:
            print(f"Failed to access {current_dir}: Permission denied")
            continue  # Skip the current directory if there's an error

    return file_list

def download_file(ftp, filename, local_dir):
    local_file_path = os.path.join(local_dir, os.path.basename(filename))
    with open(local_file_path, 'wb') as local_file:
        ftp.retrbinary(f'RETR {filename}', local_file.write)
    print(f"Downloaded: {filename}")

def main():
    with ftplib.FTP(FTP_SERVER) as ftp:
        ftp.login(FTP_USER, FTP_PASS)
        previous_files = set(get_file_list(ftp, REMOTE_DIR))

        while True:
            time.sleep(60)  # Check every 60 seconds
            current_files = set(get_file_list(ftp, REMOTE_DIR))
            new_files = current_files - previous_files

            if new_files:
                print("New files detected:", new_files)
                for file in new_files:
                    download_file(ftp, file, LOCAL_DIR)

            previous_files = current_files

if __name__ == "__main__":
    main()