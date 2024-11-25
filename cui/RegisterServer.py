import json

import questionary

from data_class.Server import Server
from cui.AbstractCUI import AbstractCUI


class RegisterServer(AbstractCUI):

    def __init__(self, servers, hosts):
        self.servers = servers
        self.hosts = hosts

    def get_command(self):
        return "server"

    def get_description(self):
        return "サーバを登録します"

    def run(self):
        if not self.hosts:
            print("ホストが登録されていません")
            return
        while True:
            if (name := questionary.text("表示名を入力してください").ask()) is None:
                return
            if self.servers.get(name) is not None:
                print("その名前は既に登録されています")
                continue
            break
        if (host := questionary.select("ホストを選択してください", choices=[host.name for host in self.hosts.values()]).ask()) is None:
            return
        if (path := questionary.text("パスを入力してください").ask()) is None:
            return
        self.servers[name] = Server(name, self.hosts[host], path)
        with open("data/servers.json", "w") as file:
            json.dump([server.to_json() for server in self.servers.values()], file, indent=4)
        print("登録が完了しました")
