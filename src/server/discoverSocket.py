import socket

SIZE = 1024
FORMAT = 'utf-8'
HOST = ''   # HAY QUE VER SI NO ES '<broadcast>' COMO EN AnnounceSocket.py


# ESTA CLASE ES SOLO PARA ESCUCHAR MENSAJES DE PUERTO Y SOCKET EN BROADCAST.
# 
class DiscoverSocket:
    # Inicializar el socket de mensajes de broadcast para el servidor
    def __init__(self, port: int):
        self.sock = socket.socket(
                        socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind((HOST, port))
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Recibimiento del mensaje "ANNOUNCE <puerto>".
    # Se asume que el string recibido en el parametro tiene ese formato.
    def receive(self) -> tuple[str, str]:
        data = ''
        while not data.endswith("\n"):
            msg, (ip, port) = self.sock.recvfrom(SIZE)
            data += msg.decode(FORMAT)
        return [data, ip]


# PARA PRUEBAS
#if __name__ == "__main__":
#    while True:
#        message = receiveFromBroadcast(2022)
#        print(message)
