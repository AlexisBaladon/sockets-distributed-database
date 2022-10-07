import socket

SIZE = 1024
FORMAT = 'utf-8'
HOST = ''   # HAY QUE VER SI NO ES '<broadcast>' COMO EN AnnounceSocket.py


# ESTA CLASE ES SOLO PARA ESCUCHAR MENSAJES DE PUERTO Y SOCKET EN BROADCAST.
# 
class DiscoverSocket:
    # Inicializar el socket de mensajes de broadcast para el servidor
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        else:
            self.sock = sock

    # Recibimiento del mensaje "ANNOUNCE <puerto>".
    # Se asume que el string recibido en el parametro tiene ese formato.
    def receive(self, puerto: int) -> tuple[str, str]:
        self.sock.bind((HOST, puerto))
        data = ''
        while not data.endswith("\n"):
            msg, (ip, port) = self.sock.recvfrom(SIZE)
            data += msg.decode(FORMAT)
        return [data, ip]

def receiveFromBroadcast(puerto: int) -> tuple[str, str]:
    disc = DiscoverSocket()
    (data, ip) = disc.receive(puerto) # Recibir respuesta
    return (data, ip)



# PARA PRUEBAS
if __name__ == "__main__":
    while True:
        message = receiveFromBroadcast(2022)
        print(message)