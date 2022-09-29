from database import *
from peerHandler import *
import zlib

class DtServer:
    def __init__(self, server_IP: str, server_port: str, descubrimiento_port: str):
        #Controlar formato antes

        self.server_IP: str = server_IP
        self.server_port: str = server_port
        self.descubrimiento_port = descubrimiento_port
        
        self.firma = '' #aplicar zlib.crc32(s)
        self.database = Database()
        self.peers = PeerHandler() #mapea IP Y PUERTO a peer (hay que ver si anda por pasaje por referencia odioso)
        return

    def determine_designated_server(self, key_crc: int):
        min_distance = abs(self.firma - key_crc)
        min_socket = self.socket #FALTA
        peers = self.peers

        peers.acquire()
        for peer_key in peers:
            peer = peers[peer_key]
            peer_distance = abs(peer.crc - key_crc)
            if peer_distance < min_distance:
                min_distance = peer_distance
                min_socket = peer.socket #FALTA
        peers.release()
        return min_socket