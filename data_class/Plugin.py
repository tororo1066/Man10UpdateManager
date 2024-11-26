import re
from typing import List, Pattern

from data_class.Server import Server


class Plugin:

    def __init__(self, name: str, remove_pattern: Pattern, source_folder: str, target_servers: List[Server], depend_updates: List[str]):
        self.name = name
        self.remove_pattern = remove_pattern
        self.source_folder = source_folder
        self.target_servers = target_servers
        self.depend_updates = depend_updates

    @staticmethod
    def from_json(servers, json):
        while True:
            try:
                target_servers = [servers[server] for server in json["target_servers"]]
                break
            except KeyError as e:
                print(f"[{json['name']}] Server {e.args[0]} is not found. Removing...")
                json["target_servers"].remove(e.args[0])

        return Plugin(json["name"], re.compile(json["remove_pattern"]), json["source_folder"], target_servers, json["depend_updates"])

    def to_json(self):
        return {"name": self.name, "remove_pattern": self.remove_pattern.pattern, "source_folder": self.source_folder, "target_servers": [server.name for server in self.target_servers], "depend_updates": self.depend_updates}

    def __str__(self):
        return f"{self.name}(remove_pattern: {self.remove_pattern.pattern}, source_folder: {self.source_folder}, target_servers: {[server.name for server in self.target_servers]}, depend_updates: {self.depend_updates})"