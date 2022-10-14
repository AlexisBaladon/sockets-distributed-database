## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de AnnounceSocket (announceSocket.py) ##

# Definicion de Imports #
import socket

# Definicion de Constantes #
SIZE = 1024
FORMAT = 'utf-8'
HOST = socket.gethostbyname(socket.gethostname())
BROADCAST = '<broadcast>'

# Definicion clase UDPSocket #
class UDPSocket:
    # Inicializar el socket de mensajes de broadcast para el servidor
    def __init__(self, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.port = port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind((HOST, port))

    # Envío del mensaje "ANNOUNCE <puerto>".
    # Se asume que el string recibido en el parametro tiene ese formato.
    def send(self, msg: str, descubrimiento_port: int):
        data = msg.encode(FORMAT)
        if (len(data) == 0):
            raise RuntimeError("Empty message sent")
        sent = self.sock.sendto(data, (BROADCAST, descubrimiento_port))
        sent = self.sock.sendto(data, (BROADCAST, 2027)) #aca va puerto de discover
        sent = self.sock.sendto(data, (BROADCAST, 2037)) #agregar mas de ser necesario
        sent = self.sock.sendto(data, (BROADCAST, 2047))
        if (sent == 0):
            raise RuntimeError("Socket connection broken")

    # Recibimiento del mensaje "ANNOUNCE <puerto>".
    # Se asume que el string recibido en el parametro tiene ese formato.
    def receive(self) -> tuple[str, str]:
        msg, (ip, port) = self.sock.recvfrom(SIZE)
        data = msg.decode(FORMAT)
        return [data, ip]