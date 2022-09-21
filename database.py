class Database:
    def __init__(self):
        self.database: dict(str) = {}
        return

    def get(self, key: str):
        return self.database[key]

    def set(self, key: str, value: str):
        self.database[key] = value
        return

    def delete(self, key: str):
        del self.database[key]
        return