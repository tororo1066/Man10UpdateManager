import paramiko


class Host:
    def __init__(self, name, host, user, password, local=False):
        self.name = name
        self.host = host
        self.user = user
        self.password = password
        self.local = local

    @staticmethod
    def from_json(json):
        return Host(json["name"], json["host"], json["user"], json["password"], json.get("local", False))

    def to_json(self):
        return {"name": self.name, "host": self.host, "user": self.user, "password": self.password, "local": self.local}

    def __str__(self):
        return f"{self.name}(host: {self.host}, user: {self.user}, password: MASKED, local: {self.local})"

    def create_ssh_client(self) -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.load_system_host_keys()
        client.connect(hostname=self.host, username=self.user, password=self.password)
        return client