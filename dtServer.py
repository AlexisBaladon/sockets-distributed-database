from database import *
import zlib

class DtServer:
    #Struct que representa a un server conocido.
    #Podría además incluir el socket persistente.
    class Peer:
        def __init__(self, server_IP: str, server_port: str, crc: int):
            self.server_IP: str = server_IP
            self.server_port: str = server_port
            self.crc = crc
            return

    def __init__(self, server_IP: str, server_port: str, descubrimiento_port: str):
        #Controlar formato antes

        self.server_IP: str = server_IP
        self.server_port: str = server_port
        self.descubrimiento_port = descubrimiento_port
        
        self.firma = '' #aplicar zlib.crc32(s)
        self.database = Database()
        self.peers: dict(str, self.Peer) = {} #mapea IP Y PUERTO a peer (hay que ver si anda por pasaje por referencia odioso)
        return