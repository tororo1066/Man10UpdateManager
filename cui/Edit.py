import json

import questionary
from questionary import Choice

from cui.AbstractCUI import AbstractCUI


class Edit(AbstractCUI):

    def __init__(self, hosts, plugins, servers):
        self.hosts = hosts
        self.plugins = plugins
        self.servers = servers

    def get_command(self):
        return "edit"

    def get_description(self):
        return "登録されているホスト/サーバ/プラグインを編集します"

    def run(self):
        if (target := questionary.select("編集するものを選択してください", choices=["ホスト", "サーバー", "プラグイン"]).ask()) is None:
            return
        if target == "ホスト":
            self.edit_host()
        elif target == "サーバー":
            self.edit_server()
        elif target == "プラグイン":
            self.edit_plugin()

    def edit_host(self):
        if not self.hosts:
            print("ホストが登録されていません")
            return
        print("編集するホストを選択してください")
        if (name := questionary.select("ホストを選択してください",
                                       choices=[host.name for host in self.hosts.values()]).ask()) is None:
            return
        host = self.hosts[name]
        print("編集する項目を選択してください")
        while True:
            if (selected := questionary.select("編集する項目を選択してください",
                                               choices=["ホスト名", "ユーザ名", "パスワード", "保存"]).ask()) is None:
                return
            elif selected == "ホスト名":
                if (new_host := questionary.text("新しいホスト名を入力してください").ask()) is None:
                    return
                host.host = new_host
            elif selected == "ユーザ名":
                if (new_user := questionary.text("新しいユーザ名を入力してください").ask()) is None:
                    return
                host.user = new_user
            elif selected == "パスワード":
                if (new_password := questionary.password("新しいパスワードを入力してください").ask()) is None:
                    return
                host.password = new_password
            elif selected == "保存":
                break
        with open("data/hosts.json", "w") as file:
            json.dump([host.to_json() for host in self.hosts.values()], file, indent=4)
        print("編集が完了しました")

    def edit_server(self):
        if not self.servers:
            print("サーバーが登録されていません")
            return
        print("編集するサーバーを選択してください")
        if (name := questionary.select("サーバーを選択してください",
                                       choices=[server.name for server in self.servers.values()]).ask()) is None:
            return
        server = self.servers[name]
        print("編集する項目を選択してください")
        while True:
            if (selected := questionary.select("編集する項目を選択してください",
                                               choices=["ホスト", "パス", "保存"]).ask()) is None:
                return
            elif selected == "ホスト":
                if (new_host := questionary.select("新しいホストを選択してください",
                                                   choices=[host.name for host in self.hosts.values()]).ask()) is None:
                    return
                server.host = new_host
            elif selected == "パス":
                if (new_path := questionary.path("新しいパスを入力してください").ask()) is None:
                    return
                server.path = new_path
            elif selected == "保存":
                break
        with open("data/servers.json", "w") as file:
            json.dump([server.to_json() for server in self.servers.values()], file, indent=4)
        print("編集が完了しました")

    def edit_plugin(self):
        if not self.plugins:
            print("プラグインが登録されていません")
            return
        print("編集するプラグインを選択してください")
        if (name := questionary.select("プラグインを選択してください",
                                       choices=[plugin.name for plugin in self.plugins.values()]).ask()) is None:
            return
        plugin = self.plugins[name]
        print("編集する項目を選択してください")
        while True:
            if (selected := questionary.select("編集する項目を選択してください",
                                               choices=["削除するファイルの正規表現", "プラグインが入っているフォルダのパス", "適用するサーバー", "依存するプラグイン", "保存"]).ask()) is None:
                return
            elif selected == "削除するファイルの正規表現":
                if (new_remove_pattern := questionary.text("削除するファイルの正規表現を入力してください").ask()) is None:
                    return
                plugin.remove_pattern = new_remove_pattern
            elif selected == "プラグインが入っているフォルダのパス":
                if (new_source_folder := questionary.path("プラグインが入っているフォルダのパスを入力してください",).ask()) is None:
                    return
                plugin.source_folder = new_source_folder
            elif selected == "適用するサーバー":
                if (new_target_servers := questionary.checkbox("適用するサーバーを選択してください",
                                                              choices=[Choice(server.name, checked=server in plugin.target_servers) for server in self.servers.values()]).ask()) is None:
                    return
                plugin.target_servers = [server for server in self.servers.values() if server.name in new_target_servers]
            elif selected == "依存するプラグイン":
                if (new_depend_updates := questionary.checkbox("依存するプラグインを選択してください",
                                                             choices=[Choice(plugin.name, checked=plugin in plugin.depend_updates) for plugin in self.plugins.values()]).ask()) is None:
                    return
                plugin.depend_updates = [plugin for plugin in self.plugins.values() if plugin.name in new_depend_updates]
            elif selected == "保存":
                break
        with open("data/plugins.json", "w") as file:
            json.dump([plugin.to_json() for plugin in self.plugins.values()], file, indent=4)
        print("編集が完了しました")