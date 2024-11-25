import json

from data_class.Host import Host
from cui.AbstractCUI import AbstractCUI
import questionary


class RegisterHost(AbstractCUI):

    def __init__(self, hosts):
        self.hosts = hosts

    def get_command(self):
        return "host"

    def get_description(self):
        return "ホストを登録します"

    def run(self):
        while True:
            if (name := questionary.text("表示名を入力してください").ask()) is None:
                return
            if self.hosts.get(name) is not None:
                print("その名前は既に登録されています")
                continue
            break
        if questionary.confirm("ローカル上ですか？").ask():
            self.hosts[name] = Host(name, "", "", "", True)
        else:
            if (host := questionary.text("ホスト名を入力してください").ask()) is None:
                return
            if (user := questionary.text("ユーザ名を入力してください").ask()) is None:
                return
            if (password := questionary.password("パスワードを入力してください").ask()) is None:
                return
            self.hosts[name] = Host(name, host, user, password)
        with open("data/hosts.json", "w") as file:
            json.dump([host.to_json() for host in self.hosts.values()], file, indent=4)
        print("登録が完了しました")

