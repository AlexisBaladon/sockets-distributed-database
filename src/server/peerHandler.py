## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Peer y PeerHandler (peerHandler.py) ##

# Definicion de Imports #
from threading import Lock
from datetime import datetime
from src.client.clientSocket import ClientSocket

# Definicion clase Peer #
class Peer:
    def __init__(self, ip: str, datos_port: int, socket: ClientSocket, crc: int):
        self.lock = Lock()
        self.ip: str = ip
        self.datos_port: int = datos_port
        self.socket: ClientSocket = socket
        self.crc: int = crc
        self.last_announce_time: datetime = datetime.now()
        return

    def get_data(self, message) -> str:
        with self.lock:
            self.socket.send(message)
            data = self.socket.receive()
        return data 
    
    ################################
    # DE USO EXCLUSIVO PARA PRUEBAS
    ################################
    def show(self):
        print(self.server_IP + '   ' + self.server_port + '   ' + str(self.crc))
        return
    #################################

# Definicion clase PeerHandler #
class PeerHandler:
    def __init__(self, peers: dict = {}):
        self.lock = Lock()
        self.peers: dict = peers

    def get_peers(self):
        with self.lock:
            peers = list(self.peers.values())
        return peers

    def get_peers_keys(self):
        with self.lock:
            keys = list(self.peers.keys())
        return keys

    def get_peer_by_key_format(self, key_format):
        with self.lock:
            value = self.peers[key_format]
        return value

    def get_peer(self, addr, port):
        with self.lock:
            value = self.peers[self.__format_key(addr, port)]
        return value
        
    def set_peer(self, addr, port, peer: Peer, lock = True):
        if lock:
            self.lock.acquire()
        self.peers[self.__format_key(addr, port)] = peer
        if lock:
            self.lock.release()
        return

    def delete_peer(self, addr, port):
        with self.lock:
            del self.peers[self.__format_key(addr, port)]
        return

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()

    def exists(self, ip, port, lock = True):
        if lock:
            self.lock.acquire()
        exists_peer = self.__format_key(ip, port) in self.peers.keys()
        if lock:
            self.lock.release()
        return exists_peer

    # Funciones auxiliares #

    def show_peers(self):
        with self.lock:
            for p in self.peers:
                print(p)
    
    def __format_key(self, addr, port) -> str:
        return f'{addr}:{port}'