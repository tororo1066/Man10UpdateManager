import os

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