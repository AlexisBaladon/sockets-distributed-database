import socket
import traceback
import threading
from src. import parseCommand
from dtServer import DtServer

PORT = 32000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(ADDR)

class Server:
    def __init__(self):
        self.data = DtServer(SERVER, PORT, "3000")
        self.clientAttendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientAttendSocket.bind(ADDR)
        return

    def handleClient(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        clientRequest = ''
        while not clientRequest.endswith("\n"):
            msg = conn.recv(SIZE)
            clientRequest += msg.decode(FORMAT)
        print(f"[{addr}] {clientRequest}")
        try:
            response = self.data.processRequest(clientRequest)
            conn.send(response.encode(FORMAT))
        except Exception as e:
            print(f"[SERV_ERR] {str(e)}")
            traceback.print_exc() #imprime stack
            conn.send("NO\n".encode(FORMAT))
        conn.close()

def main():
    print("[STARTING] server is starting...")
    server = Server()
    server.clientAttendSocket.listen()
    print(f"[SERVER] Servidor escuchando en {SERVER}")
    while True:
        conn, addr = server.clientAttendSocket.accept()
        thread = threading.Thread(target=server.handleClient, args=(conn, addr))
        thread.start()
        print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()