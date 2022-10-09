## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Database (Database.py) ##

# Definicion de Imports #
from peerHandler import PeerHandler
from src.exceptions.methodError import MethodError
from src.server.database import Database
from src.util.utilis import parseCommand, formatResponse
import zlib

class DtServer:
    def __init__(self, ip: str, datos_port: str, announce_port: str, descubrimiento_port: str):
        self.ip = ip # Direccion SERVER
        self.datos_port = datos_port # TCP DATOS
        self.announce_port = announce_port # UDP ANNOUNCE
        self.descubrimiento_port = descubrimiento_port # UDP DESCUBRIMIENTO
        
        self.firma = zlib.crc32(f'{ip}:{datos_port}'.encode())
        self.database = Database() # Inicializacion de la base de datos
        self.peers = PeerHandler() # Mapea (IP, PUERTO_DATOS) a peer
        ()
        return

    def determine_designated_server(self, key_crc: int):
        min_distance = abs(self.firma - key_crc)
        min_socket = None #esto no va, no se necesitan sockets extra para DATOS
        #Basta tener ip y puerto del servidor almacenado y tirar un ClientSocket.py
        peers = self.peers.get_peers_keys()

        for peer_key in peers:
            peer = peers.get_peer(peer_key)
            peer_distance = abs(peer.crc - key_crc)
            if peer_distance < min_distance:
                min_distance = peer_distance
                min_socket = peer.socket #FALTA
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
                response = formatResponse(method, key)
                # Si no me pertenece

                # Realizar DATOS a otro server siendo client
            case 'DEL':
                # Si me pertenece la clave
                try:
                    self.database.delete(key)
                    print("[DATABASE] Elemento %s eliminado" % key)
                    response = formatResponse(method, key)
                except KeyError:
                    print("[DATABASE] Elemento %s no encontrado" % key)
                    response = formatResponse(None, None)
                # Si no me pertenece
                # Realizar DATOS a otro server siendo client
            case _:
                raise MethodError("Metodo %s no soportado" % method)
        return response