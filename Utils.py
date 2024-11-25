import os
from typing import Pattern

from data_class.Server import Server


def copy_files(src_folder: str, dest: str, dest_server: Server):
    try:
        client = dest_server.create_ssh_client()
        print("Connected to {}".format(dest_server.host.name))

        sftp = client.open_sftp()

        print("Trying to copy files from {} to {}".format(src_folder, dest_server.path + dest))
        for file in os.listdir(src_folder):
            path = os.path.join(src_folder, file)
            dest_path = os.path.join(dest_server.path, dest, file)
            print("Trying to copy {} to {}".format(path, dest_path))
            sftp.put(path, dest_path)
            print("Copied {} to {}".format(path, dest_path))

        sftp.close()
        client.close()
    except Exception as e:
        print(e)

def remove_files(pattern: Pattern, dest: str, dest_server: Server):
    try:
        client = dest_server.create_ssh_client()
        print("Connected to {}".format(dest_server.host.name))

        sftp = client.open_sftp()

        print("Trying to remove files that match {} from {}".format(pattern, os.path.join(dest_server.path, dest)))
        for file in sftp.listdir(os.path.join(dest_server.path, dest)):
            file_path = sftp.normalize(os.path.join(dest_server.path, dest, file))
            print("Checking {}".format(file))
            if os.path.isfile(file_path) and pattern.match(file):
                print("Trying to remove {}".format(file))
                sftp.remove(file_path)
                print("Removed {}".format(file))

        sftp.close()
        client.close()
    except Exception as e:
        print(e)