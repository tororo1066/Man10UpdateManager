class Host:
    def __init__(self, name, host, user, password):
        self.name = name
        self.host = host
        self.user = user
        self.password = password

    @staticmethod
    def from_json(json):
        return Host(json["name"], json["host"], json["user"], json["password"])

    def to_json(self):
        return {"name": self.name, "host": self.host, "user": self.user, "password": self.password}

    def __str__(self):
        return f"{self.name}(host: {self.host}, user: {self.user}, password: MASKED)"