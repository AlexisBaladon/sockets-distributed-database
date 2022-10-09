## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Database (Database.py) ##

# Definicion de Imports #
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
    
    ##################################
    # Nueva (By Mathias)
    ##################################
    def get_all(self):
        with self.lock:
            values = self.database
        return values
    
    ##################################
    # De uso exclusivo para pruebas
    ##################################
    def show(self):
        for i in self.database:
            print(i + '   ' + self.get(i))
        return