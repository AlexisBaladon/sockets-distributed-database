import threading
import traceback
from dtServer import DtServer
from datos import client_attention_DATOS
from descubrimiento import ANNOUNCE, DISCOVER
from src.client.clientSocket import ClientSocket
import socket
import getopt, sys
from src.client.clientSocket import getLocalhost
from src.server import AnnounceSocket, DiscoverSocket

PORT = 32000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

HELP = ["client.py [options] | <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n",
    (" ServerIP:        Dirección IP del servidor al que se desea conectar\n"
    "  ServerPort:      Puerto del servidor al que se desea conectar\n"
    "  Op:              Operación a realizar: GET, SET o DEL\n"
    "  Key:             Clave del valor que se desea leer, escribir o borrar\n"
    "  Value:           Valor a almacenar. Solo al usar metodo SET\n\n"
    "Options:\n  -h:    Imprime el texto de ayuda")]

def handle_args(argv):
    try:
        opts, args = getopt.getopt(argv,"h")
    except getopt.GetoptError:
        print(HELP[0])
        return None
    if (('-h', '') in opts):
        print(HELP[0], HELP[1])
        return None
    if (len(args) > 5):
        print("[ATENCION] Demasiados argumentos")
        print(HELP[0])
        return None
    if (len(args) < 4):
        print("[ATENCION] Argumentos faltantes")
        print(HELP[0])
        return None
    if (len(args) == 4):
        args.append('') #Qué es esto??
    if (args[0] == 'localhost'): #Esto no anda por si solo?
        args[0] = getLocalhost()
    return None

def handle_discover(conn, server):
    print(f"[DISCOVER PROTOCOL ON]")
    try:
        DISCOVER(server)
    except Exception as e:
        print(f"[DISCOVER_SERV_ERR] {str(e)}")
        traceback.print_exc()
    conn.close()

def handle_announce(conn, server):
    print(f"[ANNOUNCE PROTOCOL ON]")
    try:
        ANNOUNCE(server)
    except Exception as e:
        print(f"[ANNOUNCE_SERV_ERR] {str(e)}")
        traceback.print_exc()
    conn.close()

def handle_client(conn, server):
    addr = server.ip
    print(f"[NEW CONNECTION] {addr} connected.")
    clientRequest = 'conn.receive()'
    print(f"[{addr}] {clientRequest}")
    try:
        response = server.processRequest(clientRequest)
        conn.send(response.encode(FORMAT))
    except Exception as e:
        print(f"[SERV_ERR] {str(e)}")
        traceback.print_exc()
        conn.send("NO\n".encode(FORMAT))
    conn.close()


if __name__ == "__main__":
    ip, port = handle_args(sys.argv)
    print("[STARTING] server is starting...")
    server = DtServer(ip, port, PORT) #Puerto de descubrimiento?
    announce_udp_socket = AnnounceSocket()
    discover_udp_socket = DiscoverSocket()
    print(f"[SERVER] Servidor escuchando en {SERVER}")
    thread_announce = threading.Thread(handle_announce, announce_udp_socket, server)
    thread_discover = threading.Thread(handle_discover, discover_udp_socket, server)

    while True:
        datos_tcp_socket = ClientSocket()
        thread_tcp = threading.Thread(handle_client, server, datos_tcp_socket)
        #start
        print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 2}")