import json

import questionary

from cui.AbstractCUI import AbstractCUI


class Remove(AbstractCUI):

        def __init__(self, hosts, plugins, servers):
            self.hosts = hosts
            self.plugins = plugins
            self.servers = servers

        def get_command(self):
            return "remove"

        def get_description(self):
            return "登録されているホスト/サーバ/プラグインを削除します"

        def run(self):
            if (target := questionary.select("削除するものを選択してください", choices=["ホスト", "サーバー", "プラグイン"]).ask()) is None:
                return
            if target == "ホスト":
                self.remove_host()
            elif target == "サーバー":
                self.remove_server()
            elif target == "プラグイン":
                self.remove_plugin()

        def remove_host(self):
            if not self.hosts:
                print("ホストが登録されていません")
                return
            print("削除するホストを選択してください")
            if (name := questionary.select("ホストを選択してください",
                                        choices=[host.name for host in self.hosts.values()]).ask()) is None:
                return
            if questionary.confirm("本当に削除しますか？ このホストに依存するサーバーも削除されます").ask():
                for server in self.servers.values():
                    if server.host == self.hosts[name]:
                        print(f"{server.name}を削除しました")
                        del self.servers[server.name]
                del self.hosts[name]
                with open("data/hosts.json", "w") as file:
                    json.dump([host.to_json() for host in self.hosts.values()], file, indent=4)
                with open("data/servers.json", "w") as file:
                    json.dump([server.to_json() for server in self.servers.values()], file, indent=4)
                print("削除が完了しました")

        def remove_server(self):
            if not self.servers:
                print("サーバーが登録されていません")
                return
            print("削除するサーバーを選択してください")
            if (name := questionary.select("サーバーを選択してください",
                                        choices=[server.name for server in self.servers.values()]).ask()) is None:
                return
            if questionary.confirm("本当に削除しますか？").ask():
                for plugin in self.plugins.values():
                    if self.servers[name] in plugin.target_servers:
                        plugin.target_servers.remove(self.servers[name])
                        print(f"{plugin.name}の依存先から{name}を削除しました")
                del self.servers[name]
                with open("data/servers.json", "w") as file:
                    json.dump([server.to_json() for server in self.servers.values()], file, indent=4)
                with open("data/plugins.json", "w") as file:
                    json.dump([plugin.to_json() for plugin in self.plugins.values()], file, indent=4)
                print("削除が完了しました")

        def remove_plugin(self):
            if not self.plugins:
                print("プラグインが登録されていません")
                return
            print("削除するプラグインを選択してください")
            if (name := questionary.select("プラグインを選択してください",
                                        choices=[plugin.name for plugin in self.plugins.values()]).ask()) is None:
                return
            if questionary.confirm("本当に削除しますか？").ask():
                for plugin in self.plugins.values():
                    if name in plugin.depend_updates:
                        plugin.depend_updates.remove(name)
                        print(f"{plugin.name}の依存先から{name}を削除しました")
                del self.plugins[name]
                with open("data/plugins.json", "w") as file:
                    json.dump([plugin.to_json() for plugin in self.plugins.values()], file, indent=4)
                print("削除が完了しました")