import json
import re

from data_class.Plugin import Plugin
from cui.AbstractCUI import AbstractCUI
import questionary


class RegisterPlugin(AbstractCUI):

    def __init__(self, plugins, servers):
        self.plugins = plugins
        self.servers = servers

    def get_command(self):
        return "plugin"

    def get_description(self):
        return "プラグインを登録します"

    def run(self):
        if not self.servers:
            print("サーバが登録されていません")
            return
        while True:
            if (name := questionary.text("表示名を入力してください").ask()) is None:
                return
            if self.plugins.get(name) is not None:
                print("その名前は既に登録されています")
                continue
            break

        if (source_folder := questionary.text("プラグインが入っているフォルダのパスを入力してください").ask()) is None:
            return
        if (target_servers := questionary.checkbox("適用するサーバを選択してください", choices=[server.name for server in self.servers.values()]).ask()) is None:
            return
        if (remove_pattern := questionary.text("削除するファイルの正規表現を入力してください").ask()) is None:
            return
        if self.plugins:
            if (
            depend_updates := questionary.checkbox("このプラグインを適用する際に更新するプラグインを選択してください",
                                                   choices=[plugin.name for plugin in
                                                            self.plugins.values()]).ask()) is None:
                return
        else:
            depend_updates = []
        self.plugins[name] = Plugin(name, re.compile(remove_pattern), source_folder, [self.servers[server] for server in target_servers], depend_updates)
        with open("data/plugins.json", "w") as file:
            json.dump([plugin.to_json() for plugin in self.plugins.values()], file, indent=4)
        print("登録が完了しました")