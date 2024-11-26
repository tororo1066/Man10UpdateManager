import os
import shutil
from typing import Pattern, Dict, List

from data_class.Host import Host
from data_class.Plugin import Plugin
from data_class.Server import Server

def copy_files(hosts: Dict[str, Host], servers: Dict[str, Server], plugins: Dict[str, Plugin], update_servers: List[str], update_plugins: List[str]):
    group_by_host = {}
    for server_name in update_servers:
        server = servers[server_name]
        if server.host.name not in group_by_host:
            group_by_host[server.host.name] = []
        group_by_host[server.host.name].append(server)

    for _plugin in list(update_plugins):
        for depend in plugins[_plugin].depend_updates:
            if depend not in update_plugins:
                update_plugins.append(depend)

    clients = {}
    for host_name in group_by_host:
        host = hosts[host_name]
        clients[host_name] = host.create_ssh_client()
        print(f"{host_name}に接続しました")


    for plugin_name in update_plugins:
        plugin = plugins[plugin_name]
        for server in plugin.target_servers:
            if server.host.name in group_by_host:
                if server.host.local:
                    print(f"{plugin_name}を{server.name}にコピー中...")
                    for file in os.listdir(plugin.source_folder):
                        path = os.path.join(plugin.source_folder, file)
                        dest_path = os.path.join(server.path_with_plugins(), file)
                        shutil.copy(path, dest_path)
                        print(f"{path}を{dest_path}にコピーしました")
                else:
                    for client in clients:
                        if server in group_by_host[client]:
                            sftp = clients[client].open_sftp()
                            print(f"{plugin_name}を{server.name}にコピー中...")
                            for file in os.listdir(plugin.source_folder):
                                path = os.path.join(plugin.source_folder, file)
                                dest_path = os.path.join(server.path_with_plugins(), file)
                                sftp.put(path, dest_path)
                                print(f"{path}を{dest_path}にコピーしました")
                            sftp.close()

    for client in clients:
        clients[client].close()

def remove_files(hosts: Dict[str, Host], servers: Dict[str, Server], plugins: Dict[str, Plugin], update_servers: List[str], update_plugins: List[str]):
    group_by_host = {}
    for server_name in update_servers:
        server = servers[server_name]
        if server.host.name not in group_by_host:
            group_by_host[server.host.name] = []
        group_by_host[server.host.name].append(server)

    for _plugin in list(update_plugins):
        for depend in plugins[_plugin].depend_updates:
            if depend not in update_plugins:
                update_plugins.append(depend)

    clients = {}
    for host_name in group_by_host:
        host = hosts[host_name]
        clients[host_name] = host.create_ssh_client()
        print(f"{host_name}に接続しました")

    for plugin_name in update_plugins:
        plugin = plugins[plugin_name]
        for server in plugin.target_servers:
            if server.host.name in group_by_host:
                if server.host.local:
                    print(f"{plugin_name}を{server.name}から削除中...")
                    for file in os.listdir(server.path_with_plugins()):
                        file_path = os.path.join(server.path_with_plugins(), file)
                        if os.path.isfile(file_path) and plugin.remove_pattern.match(file):
                            os.remove(file_path)
                            print(f"{file_path}を削除しました")
                else:
                    for client in clients:
                        if server in group_by_host[client]:
                            sftp = clients[client].open_sftp()
                            print(f"{plugin_name}を{server.name}から削除中...")
                            for file in sftp.listdir(server.path_with_plugins()):
                                file_path = sftp.normalize(os.path.join(server.path_with_plugins(), file))
                                if os.path.isfile(file_path) and plugin.remove_pattern.match(file):
                                    sftp.remove(file_path)
                                    print(f"{file_path}を削除しました")
                            sftp.close()

    for client in clients:
        clients[client].close()






# def copy_files(src_folder: str, dest: str, dest_server: Server):
#     if dest_server.host.local:
#         copy_files_local(src_folder, os.path.join(dest_server.path_with_plugins(), dest))
#         return
#     try:
#         client = dest_server.host.create_ssh_client()
#         print(f"{dest_server.host.name}に接続しました")
#
#         sftp = client.open_sftp()
#
#         print(f"{src_folder}から{os.path.join(dest_server.path_with_plugins(), dest)}にファイルをコピー中...")
#         for file in os.listdir(src_folder):
#             path = os.path.join(src_folder, file)
#             dest_path = os.path.join(dest_server.path_with_plugins(), dest, file)
#             sftp.put(path, dest_path)
#             print(f"{path}を{dest_path}にコピーしました")
#
#         sftp.close()
#         client.close()
#     except Exception as e:
#         print(e)
#
# def remove_files(pattern: Pattern, dest: str, dest_server: Server):
#     if dest_server.host.local:
#         remove_files_local(pattern, os.path.join(dest_server.path_with_plugins(), dest))
#         return
#     try:
#         client = dest_server.host.create_ssh_client()
#         print(f"{dest_server.host.name}に接続しました")
#
#         sftp = client.open_sftp()
#
#         print(f"{os.path.join(dest_server.path, dest)}から{pattern.pattern}にマッチするファイルを削除中...")
#         for file in sftp.listdir(os.path.join(dest_server.path_with_plugins(), dest)):
#             file_path = sftp.normalize(os.path.join(dest_server.path_with_plugins(), dest, file))
#             if os.path.isfile(file_path) and pattern.match(file):
#                 sftp.remove(file_path)
#                 print(f"{file_path}を削除しました")
#
#         sftp.close()
#         client.close()
#     except Exception as e:
#         print(e)

def copy_files_local(src_folder: str, dest: str):
    print(f"{src_folder}から{dest}にファイルをコピー中...")
    for file in os.listdir(src_folder):
        path = os.path.join(src_folder, file)
        dest_path = os.path.join(dest, file)
        shutil.copy(path, dest_path)
        print(f"{path}を{dest_path}にコピーしました")

def remove_files_local(pattern: Pattern, dest: str):
    print(f"{dest}から{pattern.pattern}にマッチするファイルを削除中...")
    for file in os.listdir(dest):
        if os.path.isfile(os.path.join(dest, file)) and pattern.match(file):
            os.remove(os.path.join(dest, file))
            print(f"{file}を削除しました")