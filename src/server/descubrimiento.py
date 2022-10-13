## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Descubrimiento (descubrimiento.py) ##

# Definicion de Imports #
import re, time, zlib
from src.client.clientSocket import ClientSocket
from src.server.dtServer import DtServer
from src.server.peerHandler import Peer
from src.server.announceSocket import AnnounceSocket
from src.server.discoverSocket import DiscoverSocket
from src.util.utilis import genMsgDatos, is_minimum

# Definicion de Constantes #
SLEEP_TIME = 5 # Tiempo de espera para enviar mensaje de broadcast ANNOUNCE
SIZE = 1024 # Tamanio del buffer del mensaje
FORMAT = 'utf-8' # Formato del mensaje

# Thread recibe y establece nueva conexion
def DISCOVER(server: DtServer, conn: DiscoverSocket):
    while True:
        # Escucha bloqueante por mensaje broadcast de algún peer.
        (msg, ip) = conn.receive()
        # Parsea el mensaje 'ANNOUNCE <port>', devolviendo la lista ['ANNOUNCE', <port>], o None, None.
        (method, port) = parse_command_ANNOUNCE(msg)
        #FALTA TODO: TODO PERO POR 2: Falta chequear que la pareja (ip, puerto)
        #No este en la lista de peers
        if (ip != server.ip or int(port) != server.datos_port):
            server.peers.acquire()
            if server.peers.exists(ip, port, lock=False):
                server.peers.release()
            else:
                server.peers.release()
                print(msg, ip)
                # Si ya el primer elemento en esta lista de parseo es "None", es 
                # porque el mensaje recibido tiene el formato correcto.
                if method is not None:                
                    # Abre una conexión TCP al puerto dado para soportar DATOS.
                    socket_datos = ClientSocket()
                    socket_datos.connect(ip, int(port))

                    # Actualizar lista de server.
                    crc_server_nuevo = zlib.crc32(f'{ip}:{port}'.encode())
                    nuevo_peer = Peer(ip, port, socket_datos, crc_server_nuevo)
                    server.peers.acquire()
                    server.peers.set_peer(ip, int(port), nuevo_peer, lock = False)
                    server.peers.release()
                    print("[DSCV] Se ha conectado con el nuevo peer ", ip, port)

                    # Calcular las keys a enviar al nuevo peer
                    keys_enviar = recalculate_values(server, crc_server_nuevo)
                    # Enviar y borrar de la base las keys anteriores
                    try:
                        keys_err = deliver_values(server, keys_enviar, nuevo_peer)
                        print(("[DSCV] Se enviaron ", len(keys_enviar) - len(keys_err)), 
                        " datos con exito a ", ip, port, ". Envios erroneos: ", len(keys_err))
                    except RuntimeError as e:
                        print("[DSCV_ERR] " + str(e))
    return

# Thread envia
def ANNOUNCE(server: DtServer, conn: AnnounceSocket):
    msg = format_command_ANNOUNCE(server.datos_port)
    while True:
        #aviso que existo en broadcast cada 30 segundos
        conn.send(msg, server.descubrimiento_port)
        time.sleep(SLEEP_TIME)
    return

# NOTA DE MIGUE, FAVOR LEER:
# Este es el nuevo recalculate_values que hice:
# Si se llama a esta funcion es porque se descubrio un solo servidor nuevo.
# Por lo tanto, solo es necesario comparar la distancia del CRC32 de las keys
# con el server nuevo, si este es menor a la distancia con el server actual
# recien ahi se mandan las claves (NO SE RECALCULA NADA! LOS VALORES CRC SON CONSTANTES!)
def recalculate_values(server: DtServer, crc_new_server: int) -> set:
    claves_a_enviar = set()
    claves_actuales = server.database.get_all()
    for key in claves_actuales:
        # Se usa el not en el if para hacer que la clave quede en el server actual
        # en caso de que la distancia entre ambos servers con la key sea la misma
        if not (is_minimum(zlib.crc32(key.encode()), server.firma, crc_new_server)):
            claves_a_enviar.add(key)
    return claves_a_enviar

# Envia las claves 'keys_to_deliver' al peer 'new_server_peer'
# Luego de enviada una clave, se la borra de la base de datos del server actual
# Si se rompe el socket con el peer, o ocurre un error inesperado se lanza RuntimeError
def deliver_values(server: DtServer, keys_to_deliver: set, new_server_peer: Peer) -> set:
    keys_with_errors = set()
    for key in keys_to_deliver:
        try:
            # Generamos la request para enviar la key al server nuevo
            req = genMsgDatos('SET', key, server.database.get(key))
            # Enviamos la key con su value al server nuevo, obtenemos respuesta
            resp = new_server_peer.get_data(req)
            if (resp == "OK\n"):
                # Dato enviado correctamente, se elimina de la database actual
                server.database.delete(key)
            else:
                # Ocurrio un error, no se envia el dato y se la deja en el server
                keys_with_errors.add(key)
        except (TimeoutError, RuntimeError):
            # Se rompio la conexion con el servidor nuevo, parar!
            raise RuntimeError("La conexion de ", server.ip, " con el peer con firma ", str(hex(new_server_peer.crc)), " se rompio")
        except Exception:
            # Ocurrio un error inesperado... Parar!
            raise RuntimeError("Ocurrio un error inesperado al enviar las claves a un peer desde ", server.ip)
    return keys_with_errors

# Funciones auxiliares #

def format_command_ANNOUNCE(port: str) -> str:
    return f"ANNOUNCE {port}\n"

def parse_command_ANNOUNCE(command: str) -> tuple[str, str]:
    regex_method = {
        "ANNOUNCE": r'^ANNOUNCE (\d|\w+)\n$',
    }
    for method in regex_method:
        regex = re.compile(regex_method[method])
        method_match = regex.match(command)
        if method_match is not None:
            value = method_match.group(1)
            return method, value
    return None, None
