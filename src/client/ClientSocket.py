## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de ClientSocket (ClientSocket.py) ##

# Definicion de Imports #
import socket

# Definicion de Constantes #
SIZE = 1024 # Tamanio del buffer del mensaje
FORMAT = 'utf-8' # Formato del mensaje

dict server.listaSockets

for compas in Peers:
    socketcompa = clientsocket()
    socketcompa.connect(compaip, puertocompa)
    listaSockets.append((compas, socketcompa))

class ClientSocket:
    # Inicializar el socket del cliente
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta con un socket remoto en host:port
    # Nota: Lanza las excepciones TimeoutError y InterruptedError
    def connect(self, host, port):
        self.sock.connect((host, port))

    # Precondicion: se debe estar conectado con el socket remoto
    def send(self, msg):
        data = msg.encode(FORMAT)
        if (len(data) == 0):
            raise RuntimeError("Empty message sent")
        sent = self.sock.send(data)
        if (sent == 0):
            raise RuntimeError("Socket connection broken")
            
    # Precondicion: se debe estar conectado con el socket remoto
    def receive(self) -> str:
        data = ''
        while not data.endswith("\n"):
            msg = self.sock.recv(SIZE)
            data += msg.decode("utf-8")
        return data

    # Finalizar conexion con el socket remoto
    def close(self):
        self.sock.close()

# Obtener localhost
def getLocalhost():
    return socket.gethostbyname(socket.gethostname())

# Envia el mensaje 'msg' al socket remoto en addr:port siguiendo el 
#   Protocolo DATOS
# Finaliza la conexion y retorna la respuesta por parte del servidor.
def sendMsgDatos(addr: str, port: int, msg: str) -> str:
    data = ''
    client = ClientSocket() # Obtener el socket
    client.connect(addr, port) # Establecer conexion
    client.send(msg) # Enviar mensaje (DATOS)
    data = client.receive() # Recibir respuesta
    client.close() # Finalizar conexion
    return data