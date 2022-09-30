import socket 
import threading
from datos import parseCommand

PORT = 2022
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def initServer():
    #DtServer("12","p","puerto_des")

    return



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    data = ''
    while not data.endswith("\n"):
        msg = conn.recv(SIZE)
        data += msg.decode(FORMAT)
    print(f"[{addr}] {data}")
    conn.send("Msg received\n".encode(FORMAT))
    conn.close()

def main():
    server.listen()
    print(f"[SERVER] Servidor escuchando en {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
main()