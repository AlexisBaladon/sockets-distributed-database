import socket
import zlib

SIZE = 1024
FORMAT = 'utf-8'
HOST = '<broadcast>'


# ESTA CLASE ES SOLO PARA CREAR EL SOCKET UDP PARA ENVIAR MENSAJES DE BROADCAST.
# SE SUPONE QUE NO RECIBE NADA PORQUE SERAN LOS PEERS QUIENES SE ENCARGUEN DE ABRIR UNA PETICION PARA DATOS CON EL PUERTO ENVIADO.
class AnnounceSocket:
    # Inicializar el socket de mensajes de broadcast para el servidor
    def __init__(self, port: int):
        self.sock = socket.socket(
                        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.port = port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))

    # Envío del mensaje "ANNOUNCE <puerto>".
    # Se asume que el string recibido en el parametro tiene ese formato.
    def send(self, msg: str, descubrimiento_port: int):
        data = msg.encode(FORMAT)
        if (len(data) == 0):
            raise RuntimeError("Empty message sent")
        sent = self.sock.sendto(data, (HOST, descubrimiento_port))
        if (sent == 0):
            raise RuntimeError("Socket connection broken")

def sendMsgBroadcast(msg: str, puerto: int):
    data = ''
#    print('[CONN] Estableciendo conexion con %s:%d' % (HOST, PORT))
    ann = AnnounceSocket() # Obtener el socket
    ann.send(msg, puerto) # Enviar mensaje (DESCUBRIMIENTO)
#    print(msg, puerto)
#    print('[CONN] Mensaje enviado')

#PARA PRUEBAS
if __name__ == "__main__":

    msg = '127.0.0.1' + ':' + '2022\n'
    print(msg)
    enc_msg = msg.encode()
    #bmsg = bytes(msg, 'utf-8')
    print(hex(zlib.crc32(enc_msg)))

    ann_sock = AnnounceSocket()
    message = 'ANNOUNCE 1986\n'
    ann_sock.send(message, 2022)
