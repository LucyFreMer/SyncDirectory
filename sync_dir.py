import os
import shutil
import time
import hashlib
from datetime import datetime


def calculate_md5(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def sync_folders(source_dir, target_dir, log_file):
    with open(log_file, 'a') as log:
        for src_dir, _, files in os.walk(source_dir):
            replica_dir = src_dir.replace(source_dir, target_dir, 1)
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                log.write(f"{current_time()} - Directory created: {replica_dir}\n")
                print(f"{current_time()} - Directory created: {replica_dir}")

            for file_name in files:
                src_file = os.path.join(src_dir, file_name)
                replica_file = os.path.join(replica_dir, file_name)

                if not os.path.exists(replica_file) or calculate_md5(src_file) != calculate_md5(replica_file):
                    shutil.copy2(src_file, replica_file)
                    log.write(f"{current_time()} - File copied/updated: {replica_file}\n")
                    print(f"{current_time()} - File copied/updated: {replica_file}")

        for rep_dir, _, files in os.walk(target_dir):
            src_dir = rep_dir.replace(target_dir, source_dir, 1)
            for file_name in files:
                rep_file = os.path.join(rep_dir, file_name)
                src_file = os.path.join(src_dir, file_name)
                if not os.path.exists(src_file):
                    os.remove(rep_file)
                    log.write(f"{current_time()} - File removed: {rep_file}\n")
                    print(f"{current_time()} - File removed: {rep_file}")


def main():
    source_dir = "source_dir"
    target_dir = "target_dir"
    interval = 2  # Synchronization every 2 seconds
    log_file = "sync_log.txt"

    while True:
        sync_folders(source_dir, target_dir, log_file)
        time.sleep(interval)


if __name__ == "__main__":
    main()