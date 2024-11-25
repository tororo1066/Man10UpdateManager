import os
from typing import Pattern

from data_class.Server import Server


def copy_files(src_folder: str, dest: str, dest_server: Server):
    try:
        client = dest_server.create_ssh_client()
        print(f"{dest_server.host.name}に接続しました")

        sftp = client.open_sftp()

        print(f"{src_folder}から{os.path.join(dest_server.path, dest)}にファイルをコピー中...")
        for file in os.listdir(src_folder):
            path = os.path.join(src_folder, file)
            dest_path = os.path.join(dest_server.path, dest, file)
            sftp.put(path, dest_path)
            print(f"{path}を{dest_path}にコピーしました")

        sftp.close()
        client.close()
    except Exception as e:
        print(e)

def remove_files(pattern: Pattern, dest: str, dest_server: Server):
    try:
        client = dest_server.create_ssh_client()
        print(f"{dest_server.host.name}に接続しました")

        sftp = client.open_sftp()

        print(f"{os.path.join(dest_server.path, dest)}から{pattern}にマッチするファイルを削除中...")
        for file in sftp.listdir(os.path.join(dest_server.path, dest)):
            file_path = sftp.normalize(os.path.join(dest_server.path, dest, file))
            if os.path.isfile(file_path) and pattern.match(file):
                sftp.remove(file_path)
                print(f"{file_path}を削除しました")

        sftp.close()
        client.close()
    except Exception as e:
        print(e)