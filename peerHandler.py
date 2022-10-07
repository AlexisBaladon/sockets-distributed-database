from threading import Lock

class Peer:
    def __init__(self, server_IP: str, server_port: str, crc: int):
        self.server_IP: str = server_IP
        self.server_port: str = server_port
        self.crc = crc
        return

    ################################
    # DE USO EXCLUSIVO PARA PRUEBAS
    ################################
    def show(self):
        print(self.server_IP + '   ' + self.server_port + '   ' + str(self.crc))
        return
    ###################################

class PeerHandler:
    def __init__(self, peers: dict = {}):
        self.lock = Lock()
        self.peers: dict = peers

    def acquire(self):
        self.lock.acquire(blocking=True)
        return
    
    #USAR SOLO LUEGO DE ADQUIRIR EL MUTEX
    def get_peers(self):
        with self.lock:
            return list(self.peers.values())

    def release(self):
        self.lock.release()
        return


    #def get_peer(self, crc: str):
    #    with self.lock:
    #        value = self.peers[crc]
    #    return value
#
    #def set_peer(self, crc: str, peer: Peer):
    #    with self.lock:
    #        self.peers[crc] = peer
    #    return
#
    #def delete_peer(self, crc: str):
    #    with self.lock:
    #        del self.peers[crc]
    #    return

    
    def get_peer(self, crc: str):
        with self.lock:
            value = self.peers[crc]
        return value
    
    def get_all(self):
        with self.lock:
            value = self.peers
        return value

    def set_peer(self, peer: Peer):
        with self.lock:
            self.peers[peer.crc] = peer
        return

    def delete_peer(self, crc: str):
        with self.lock:
            del self.peers[crc]
        return

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
