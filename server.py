#!/usr/bin/python

## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Server (server.py) ##

# Definicion de Imports #
import getopt, socket, sys, threading, traceback
from src.client.clientSocket import ClientSocket, getLocalhost
from src.exceptions.argumentError import ArgumentError
from src.server.dtServer import DtServer
from src.server.descubrimiento import DISCOVER, ANNOUNCE
from src.server.udpSocket import UDPSocket
from src.util.utilis import checkIp, checkPort

# Definicion de Constantes #
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

# Definicion de Funciones #

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
    while True:
        try:
            DISCOVER(server, conn)
        except Exception as e:
            print(f"[SERV_ERR] {str(e)}")
            traceback.print_exc()
    conn.close()
    return

def handle_announce(server: DtServer, conn):
    print(f"[SERVER] ANNOUNCE PROTOCOL ON")
    while(True):
        try:
            ANNOUNCE(server, conn)
        except Exception as e:
            print(f"[SERV_ERR] {str(e)}")
            traceback.print_exc()
    conn.close()
    return

def check_token(server_crc: str, msg: str) -> bool:
    return msg == f"SRV_CONN {server_crc}\n"

def handle_client(server: DtServer, conn: ClientSocket, flag_not_server = True):
    response = "NO\n"
    try:
        msg = conn.receive()
        is_server = check_token(hex(server.firma), msg)
        if (is_server):
            conn.send("OK\n")
            handle_peer_server(server, conn)
        else:
            response = server.processRequest(msg)
        print(response)
    except Exception as e:
        print(f"[SERV_ERR] {str(e)}")
        traceback.print_exc()
    conn.send(response)
    if  flag_not_server:
        conn.close()
    return None

def handle_peer_server(server: DtServer, conn: ClientSocket):
    while True:
        handle_client(server, conn, False)
    return

def handle_datos(server: DtServer, conn: ClientSocket):
    conn.bind(server.ip, server.datos_port)
    conn.listen()
    while True:
        conn_c, addr_c = conn.accept()
        (ip, port) = conn_c.getpeername()
        print(f"[NUEVA_CONEXION] {ip}:{port} conectado.")
        thread_client = threading.Thread(target=handle_client, args=(server, ClientSocket(conn_c)), daemon=True)
        thread_client.start()
    return

# Funcion principal #

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
    announce_udp_socket = UDPSocket(server.announce_port) # Crear announce socket
    discover_udp_socket = UDPSocket(server.descubrimiento_port) # Crear discover socket
    datos_tcp_socket = ClientSocket() # Crear client socket
    thread_announce = threading.Thread(target=handle_announce, args=(server, announce_udp_socket), daemon=True)
    thread_discover = threading.Thread(target=handle_discover, args=(server, discover_udp_socket), daemon=True)
    thread_datos = threading.Thread(target=handle_datos, args=(server, datos_tcp_socket), daemon=True)
    thread_announce.start()
    thread_discover.start()
    thread_datos.start()
    print(f"[SERVER] Servidor atendiendo DATOS en {ip}:{datos_port}")
    while True:
        command = input()
        if (command == "database get all"):
            print(server.database.get_all())
        else:
            print("[CMND] Comando no es correcto")
        continue
    return

# Main Init #
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        # Si hay Cntr + C matar todos los threads
        print("[SERVER] Deteniendo servidor")