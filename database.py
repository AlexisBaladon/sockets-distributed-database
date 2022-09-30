from threading import Lock

class Database:
    def __init__(self):
        self.database: dict(str) = {}
        self.lock = Lock()
        return

    # Si la key no existe, se lanza KeyError
    def get(self, key: str) -> str:
        with self.lock:
            value = self.database[key]
        return value

    def set(self, key: str, value: str):
        with self.lock:
            self.database[key] = value
        return

    # Si la key no existe, se lanza KeyError
    def delete(self, key: str):
        with self.lock:
            del self.database[key]
        return