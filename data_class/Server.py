import os

import paramiko

from data_class.Host import Host


class Server:

    def __init__(self, name: str, host: Host, path: str):
        self.name = name
        self.host = host
        self.path = os.path.join(path, "plugins")

    @staticmethod
    def from_json(hosts, json):
        host = hosts[json["host"]]
        return Server(json["name"], host, json["path"])

    def to_json(self):
        return {"name": self.name, "host": self.host.name, "path": self.path}

    def __str__(self):
        return f"{self.name}(host: {self.host.name}, path: {self.path})"

    def create_ssh_client(self) -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(hostname=self.host.host, username=self.host.user, password=self.host.password)
        return client