#!/usr/bin/python

## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Server (server.py) ##
import socket
import getopt, sys
import threading
import traceback
from dtServer import DtServer
from descubrimiento import DISCOVER, ANNOUNCE
from src.client.clientSocket import ClientSocket, getLocalhost
from src.exceptions.argumentError import ArgumentError
from src.server.announceSocket import AnnounceSocket
from src.server.discoverSocket import DiscoverSocket
from src.util.utilis import checkIp, checkPort

DEFAULT_DATOS_PORT = 32000
DEFAULT_ANNOUNCE_PORT = 32001
DEFAULT_DISCOVER_PORT = 32002
SERVER = socket.gethostbyname(socket.gethostname())

HELP = [("client.py [options] | <ServerIP> <ServerDatosPort> "
    "[<ServerAnnouncePort>] [<ServerDiscoverPort>]\n"),
    (" ServerIP:           Dirección IP del servidor\n"
    "  ServerDatosPort:    Puerto del servidor de DATOS\n"
    "  ServerAnnouncePort: Puerto del servidor de ANNOUNCE\n"
    "  ServerDiscoverPort: Puerto del servidor de DESCUBRIMIENTO\n"
    "Options:\n  -h:    Imprime el texto de ayuda")]

def handle_args(argv):
    opts, args = getopt.getopt(argv,"h")
    if (('-h', '') in opts):
        print(HELP[0], HELP[1])
        return None, None, None, None
    if (len(args) > 4):
        raise ArgumentError("[ATENCION] Demasiados argumentos")
    if (len(args) < 2):
        raise ArgumentError("[ATENCION] Argumentos faltantes")
    addr = checkIp(args[0]) if args[0] != 'localhost' else getLocalhost()
    datos_port = checkPort(args[1]) if args[1] != 'default' else DEFAULT_DATOS_PORT
    announce_port = checkPort(args[2]) if len(args) > 2 else DEFAULT_ANNOUNCE_PORT
    discover_port = checkPort(args[3]) if len(args) > 3 else DEFAULT_DISCOVER_PORT
    return addr, datos_port, announce_port, discover_port

def handle_discover(server: DtServer, conn):
    print(f"[SERVER] DISCOVER PROTOCOL ON")
    try:
        DISCOVER(server, conn)
    except Exception as e:
        print(f"[SERV_ERR] {str(e)}")
        traceback.print_exc()
    conn.close()

def handle_announce(server: DtServer, conn):
    print(f"[SERVER] ANNOUNCE PROTOCOL ON")
    try:
        ANNOUNCE(server, conn)
    except Exception as e:
        print(f"[SERV_ERR] {str(e)}")
        traceback.print_exc()
    conn.close()

def handle_client(server: DtServer, conn: ClientSocket, addr_c: str):
    try:
        msg = conn.receive()
        response = server.processRequest(msg)
        conn.send(response)
    except Exception as e:
        print(f"[SERV_ERR] {str(e)}")
        conn.send("NO\n")
    conn.close()
    return None

def handle_datos(server: DtServer, conn: ClientSocket):
    conn.bind(server.ip, server.datos_port)
    conn.listen()
    while True:
        conn_c, addr_c = conn.accept()
        print(f"[NUEVA_CONEXION] {addr_c} conectado.")
        thread_client = threading.Thread(target=handle_client, args=(server, ClientSocket(conn_c), addr_c))
        thread_client.start()

def main(args):
    try:
        ip, datos_port, announce_port, discover_port = handle_args(args)
        if (ip == None):
            return None
    except Exception as e:
        print(f"[ATENCION] {str(e)}")
        print(HELP[0])
        return None

    # Inicializacion del server #
    server = DtServer(ip, datos_port, announce_port, discover_port) 
    announce_udp_socket = AnnounceSocket(server.announce_port) # Crear announce socket
    discover_udp_socket = DiscoverSocket(server.descubrimiento_port) # Crear discover socket
    datos_tcp_socket = ClientSocket() # Crear client socket
    thread_announce = threading.Thread(target=handle_announce, args=(server, announce_udp_socket))
    thread_discover = threading.Thread(target=handle_discover, args=(server, discover_udp_socket))
    thread_datos = threading.Thread(target=handle_datos, args=(server, datos_tcp_socket))
    thread_announce.start()
    thread_discover.start()
    thread_datos.start()
    print(f"[SERVER] Servidor atendiendo DATOS en {ip}:{datos_port}")
    while True:
        continue
    #datos_tcp_socket.close() Se encarga la libreria????????
    # Revisar en socket.python.com (url no real no entrar pls)
    #                                               ^  
    #                                               |
    #                                               |

# Main Init #
if __name__ == "__main__":
    main(sys.argv[1:])

#MAIN:
#   precondiciones---
#   thread iniciando anounce socket
#   thread iniciando discover socket
#   thread (que va a tener otros subthreads) con atencion a client (clientsocket)
#   a partir de aca, tenemos el thead "principal"
#   while (true)
#       donde chequea entradas de consola
#       puede matar el proceso dada una entrada
#       o mostrar datos del server, como por ejemplo datos de la base de datos
#       ## server.getkeys o server.getvalues, opt: server.setkeys
#
#
#        traceback.print_exc() # imprime stack