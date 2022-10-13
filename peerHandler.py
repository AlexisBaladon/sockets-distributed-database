from threading import Lock

from src.client.clientSocket import ClientSocket

class Peer:
    def __init__(self, ip: str, datos_port: int, socket: ClientSocket, crc: int):
        self.lock = Lock()
        self.ip = ip
        self.datos_port = datos_port
        self.socket = socket
        self.ip = ip
        self.port = port
        self.crc = crc
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
        
####################
# MAIN PARA PRUEBAS
####################
if __name__ == '__main__':
    peer1 = Peer('190.120.5.132', '8888', '0xA109F5')
    peer2 = Peer('120.0.15.111', '37652', '0xABCDEF')
    peer3 = Peer('10.1.1.5', '342189', '0x784C00')
    manejador_peers = PeerHandler()
    try:
        print('Cargando peers...')
        manejador_peers.set_peer(peer1)
        manejador_peers.set_peer(peer2)
        manejador_peers.set_peer(peer3)
    except:
        print('Error al setar peers.')
    try:
        print('Mostrando peers...')
        mis_peers = manejador_peers.get_all()
        for i in mis_peers:
            mis_peers[i].show()
    except:
        print('Error al mostrar los peers.')
    try:
        print('Buscando un peer...')
        res_per = manejador_peers.get_peer('0xABCDEF')
        res_per.show()
    except:
        print('No fue posible encontrar el peer.')
    try:
        print('Borrando un peer...')
        manejador_peers.delete_peer('0xABCDEF')
        mis_peers = manejador_peers.get_all()
        for i in mis_peers:
            mis_peers[i].show()
    except:
        print('Fallo al eliminar el peer...')
