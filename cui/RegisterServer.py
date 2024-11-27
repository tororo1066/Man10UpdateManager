import json

import questionary

from data_class.Server import Server
from cui.AbstractCUI import AbstractCUI


class RegisterServer(AbstractCUI):

    def __init__(self, servers, hosts, plugins):
        self.servers = servers
        self.hosts = hosts
        self.plugins = plugins

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
        if (plugins := questionary.checkbox("あらかじめ適用するプラグインを選択してください", choices=[plugin.name for plugin in self.plugins.values()]).ask()) is None:
            return
        self.servers[name] = Server(name, self.hosts[host], path)
        for plugin in plugins:
            self.plugins[plugin].target_servers.append(self.servers[name])
        server_values = [server.to_json() for server in self.servers.values()]
        with open("data/servers.json", "w") as file:
            json.dump(server_values, file, indent=4)
        plugin_values = [plugin.to_json() for plugin in self.plugins.values()]
        with open("data/plugins.json", "w") as file:
            json.dump(plugin_values, file, indent=4)
        print("登録が完了しました")
