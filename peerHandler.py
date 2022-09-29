from threading import Lock

class Peer:
    def __init__(self, server_IP: str, server_port: str, crc: int):
        self.server_IP: str = server_IP
        self.server_port: str = server_port
        self.crc = crc
        return

class PeerHandler:
    def __init__(self, peers: dict(str, Peer) = {}):
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

    
