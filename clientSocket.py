import socket

SERVER = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
PORT = 2022  # The port used by the server
ADDR = (SERVER, PORT)

SIZE = 1024 # Size of the message buffer
FORMAT = 'utf-8' # Format of the message
DISCONNECT_MESSAGE = "!DISCONNECT"

class ClientSocket:
    # Initialize the client socket
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    # Connects to a remote socket at host:port
    # Note: Raises TimeoutError and InterruptedError exceptions
    def connect(self, host, port):
        self.sock.connect((host, port))

    # Precondition: socket must be connected to a remote socket
    def send(self, msg):
        data = msg.encode(FORMAT)
        if (len(data) == 0):
            raise RuntimeError("Empty message sent")
        sent = self.sock.send(data)
        if (sent == 0):
            raise RuntimeError("Socket connection broken")
            
    # Precondition: socket must be connected to a remote socket
    def receive(self) -> str:
        data = ''
        while not data.endswith("\n"):
            print(data)
            msg = self.sock.recv(SIZE)
            data += msg.decode("utf-8")
        return data

    # Close the connection to the remote socket
    def close(self):
        self.sock.close()

    def getHost(self):
        return SERVER