import json
from typing import List, Dict

import questionary

from cui.Edit import Edit
from cui.Remove import Remove
from data_class.Host import Host
from data_class.Plugin import Plugin
from data_class.Server import Server
from cui.AbstractCUI import AbstractCUI
from cui.RegisterHost import RegisterHost
from cui.RegisterPlugin import RegisterPlugin
from cui.RegisterServer import RegisterServer

hosts: Dict[str, Host] = {}
servers: Dict[str, Server] = {}
plugins: Dict[str, Plugin] = {}

registers: List[AbstractCUI] = [
    RegisterHost(hosts),
    RegisterServer(servers, hosts),
    RegisterPlugin(plugins, servers),
    Edit(hosts, plugins, servers),
    Remove(hosts, plugins, servers)
]

if __name__ == '__main__':
    def help_commands():
        print("Commands:")
        print("  help: ヘルプを表示します")
        for _register in registers:
            print(f"  {_register.get_command()}: {_register.get_description()}")
        print("  update: プラグインを更新します")
        print("  list <host/server/plugin>: 登録されているホスト/サーバ/プラグインを表示します")
        print("  exit: 終了します")
    # Load hosts from file
    with open("./data/hosts.json") as file:
        try:
            for host in json.load(file):
                hosts[host["name"]] = Host.from_json(host)
        except json.JSONDecodeError:
            pass

    # Load servers from file
    with open("./data/servers.json") as file:
        try:
            for server in json.load(file):
                servers[server["name"]] = Server.from_json(hosts, server)
        except json.JSONDecodeError:
            pass

    # Load plugins from file
    with open("./data/plugins.json") as file:
        try:
            for plugin in json.load(file):
                plugins[plugin["name"]] = Plugin.from_json(servers, plugin)
        except json.JSONDecodeError:
            pass

    # Prepare for CUI
    print("Welcome to the plugin updater!")
    help_commands()

    while True:

        command = questionary.text("コマンドを入力してください").ask()

        if command is None or command == "exit":
            break

        if command == "help":
            help_commands()
            continue

        if command == "update":
            which = questionary.select("どちらを対象にしますか？", choices=["全て", "サーバー", "プラグイン"]).ask()
            if which is None:
                continue
            if which == "全て":
                for plugin in plugins.values():
                    plugin.update(plugins)
            elif which == "サーバー":
                if not servers:
                    print("サーバーが登録されていません")
                    continue
                update_servers = [server.name for server in servers.values()]
                if (target := questionary.checkbox("更新するサーバーを選択してください",
                                                 choices=update_servers).ask()) is None:
                    continue
                for plugin in plugins.values():
                    plugin.update(plugins, target)
            elif which == "プラグイン":
                if not plugins:
                    print("プラグインが登録されていません")
                    continue
                update_plugins = [plugin.name for plugin in plugins.values()]
                if (target := questionary.checkbox("更新するプラグインを選択してください",
                                                 choices=update_plugins).ask()) is None:
                    continue
                for plugin_name in target:
                    plugins[plugin_name].update(plugins)


        if command == "list host":
            for host in hosts.values():
                print(f"- {host}")
            continue

        if command == "list server":
            for server in servers.values():
                print(f"- {server}")
            continue

        if command == "list plugin":
            for plugin in plugins.values():
                print(f"- {plugin}")
            continue

        for register in registers:
            if command == register.get_command():
                register.run()
                break