from database import Database
from peerHandler import PeerHandler
from src.util.Utilis import parseCommand, formatResponse
from src.exceptions.MethodError import MethodError
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

    # POR AHORA SOLO PROCESA EN EL MISMO
    # Procesa la request obteniendo una respuesta acorde al protocolo DATOS
    # En caso de error con el metodo se lanza la excepcion MethodError
    def processRequest(self, request: str) -> str:
        response = ''
        (method, key, value) = parseCommand(request)
        #determine_designated_server (esta rara esa func, y no funciona
        # bien. Hay que encontrar una forma mas facil de devolver quien
        # es responzable, y no pasar un socket directo)
        match method:
            case 'GET':
                # Si me pertenece la clave
                try:
                    response = self.database.get(key)
                    print("[DATABASE] Elemento %s obtenido" % key)
                    response = formatResponse(method, response)
                except KeyError:
                    print("[DATABASE] Elemento %s no encontrado" % key)
                    response = formatResponse(None, None)
                # Si no me pertenece
                # Realizar DATOS a otro server siendo client
            case 'SET':
                # Si me pertenece la clave
                self.database.set(key, value)
                print("[DATABASE] Valor nuevo almacenado en elemento %s" % key)
                response = formatResponse(method, None)
                # Si no me pertenece
                # Realizar DATOS a otro server siendo client
            case 'DEL':
                # Si me pertenece la clave
                try:
                    self.database.get(key)
                    print("[DATABASE] Elemento %s eliminado" % key)
                    response = formatResponse(method, None)
                except KeyError:
                    print("[DATABASE] Elemento %s no encontrado" % key)
                    response = formatResponse(None, None)
                # Si no me pertenece
                # Realizar DATOS a otro server siendo client
            case _:
                raise MethodError("Metodo %s no soportado" % method)
        return response