from xml.dom import ValidationErr
from src.server.Database import Database


import re
import socket
import time
import zlib
from dtServer import DtServer
from peerHandler import Peer
from src.server.AnnounceSocket import sendMsgBroadcast
from src.server.DiscoverSocket import receiveFromBroadcast
#from src.util.Utilis import checkIp 
#from src.util.Utilis import genMsgDatos 

# Definicion de Constantes #
SIZE = 1024 # Tamanio del buffer del mensaje
FORMAT = 'utf-8' # Formato del mensaje

# Thread recibe y establece nueva conexion
def DISCOVER(server: DtServer):
    while True:
        # Escucha bloqueante por mensaje broadcast de algún peer.
        (msg, ip) = receiveFromBroadcast(server.descubrimiento_port)
        # Parsea el mensaje 'ANNOUNCE <port>', devolviendo la lista ['ANNOUNCE', <port>], o None, None.
        (method, port) = parse_command_ANNOUNCE(msg)
        # Si ya el primer elemento en esta lista de parseo es "None", es porque el mensaje recibido tiene el formato correcto.
        if method is not None:
            puerto_peer_datos = port    # Del parseo me interesa unicamente el nro. de puerto, el cual lugo utilizo para establecer comunicacion con el server anunciado para el protocolo datos.
        #CASO EN EL QUE NO:TODO    


        #actualizar lista de server.
        server_nuevo = ip + ':' + puerto_peer_datos
        enc_server_nuevo = server_nuevo.encode()
        crc_server_nuevo = hex(zlib.crc32(enc_server_nuevo))
        nuevo_peer = Peer(ip, puerto_peer_datos, str(crc_server_nuevo))
        server.peers.set_peer(nuevo_peer)

        # Abre una conexión TCP al puerto dado para soportar DATOS.
        socket_datos = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TODO: Client socket
        socket_datos.connect(ip, puerto_peer_datos)

        # Estuve pensando, y es que a lo mejor nos conviene que la clase Server (o DtServer no se) tenga un atributo como una lista para almacenar estos valores, y reutilizarlos en otro lado.
        recalculados = recalculate_values(server, crc_server_nuevo)
        deliver_values(recalculados, socket_datos)
    return

# Thread envia
def ANNOUNCE(server: DtServer):
    msg = format_command_ANNOUNCE(server.server_port)
    while True:
        #aviso que existo en broadcast cada 30 segundos
        sendMsgBroadcast(msg, server.descubrimiento_port)
        time.sleep(30)
    return

def recalculate_values(server: DtServer, crc_server_nuevo):
    # Declarar una lista de retorno, inicialmente vacia
    valores_a_transferir = dict()
    valores_servidor_actual = server.database.get_all()
    for i in valores_servidor_actual:
        clave_valor = i + ':' + valores_servidor_actual[i]
        enc_clave_valor = clave_valor.encode()
        crc_clave_valor = hex(zlib.crc32(enc_clave_valor))
        diff1 = abs(int(crc_server_nuevo, 16) - int(crc_clave_valor, 16))
        diff2 = abs(int(server.firma, 16) - int(crc_clave_valor, 16))
        if (diff1) <= (diff2):
            # En caso de haber empate de diferencias, se elige el servidor con la firma más baja como el designado a la clave.
            if int(crc_server_nuevo, 16) < int(server.firma, 16):
                # Si la firma le corresponde al nuevo servidor, se prepara la clave y su respectivo valor para ser transferido (ya armado con forma de un mensaje SET de DATOS).
                msg = 'SET ' + i + ' ' + valores_servidor_actual[i] + '\n'
                valores_a_transferir[crc_clave_valor] = msg
            # Si la firma más baja es la de este servidor, entonces no se hace nada (i.e.: conserva la <clave, valor>).
    return valores_a_transferir
    
#def deliver_values(server: DtServer, ip: str, value: str):
# Esta nueva definición asume que 'socket_abierto_datos' es parte de una conexion TCP ya hecha y abierta.
def deliver_values(diccionario_recalculados, socket_abierto_datos):
    #Adquirir peer_socket = ClientSocket
    #peer_socket.send(msg)
    #Soltar



    #se ejecuta despues de recalculate_values
    for i in diccionario_recalculados:
        socket_abierto_datos.send(diccionario_recalculados[i].encode(FORMAT))
    return

#Parsing
def format_command_ANNOUNCE(port: str) -> str:
    return f"ANNOUNCE {port}\n"

def parse_command_ANNOUNCE(command: str) -> tuple[str, str]:
    regex_method = {
        "ANNOUNCE": r'^ANNOUNCE (\d|\w+)\n$',
    }
    for method in regex_method:
        regex = re.compile(regex_method[method])
        method_match = regex.match(command)
        if method_match is not None:
            value = method_match.group(1)
            return method, value
    return None, None

# PARA PRUEBAS
if __name__ == '__main__':
#    res = parse_command_ANNOUNCE('ANNOUNCE dfs1234\n')
#    if res[0] is not None:
#        print(res)
#    else:
#        print('NNOOOUUUPPP')

    mi_server = '192.168.0.100' + ':' + '2022'
    enc_mi_server = mi_server.encode()
    crc_mi_server = hex(zlib.crc32(enc_mi_server))

    server_nuevo = '10.1.0.1' + ':' + '2022'
    enc_server_nuevo = server_nuevo.encode()
    crc_server_nuevo = hex(zlib.crc32(enc_server_nuevo))

    valores_a_transferir = dict()
    valores_servidor_actual = Database()
    valores_servidor_actual.set('clave1', 'valor1')
    crc_valor1 = hex(zlib.crc32(('clave1:valor1').encode()))
    print('Firma clave1 (y en decimal): ' + crc_valor1 + ' (' + str(int(crc_valor1, 16)) + ')')
    valores_servidor_actual.set('clave2', 'valor2')
    crc_valor2 = hex(zlib.crc32(('clave2:valor2').encode()))
    print('Firma clave2 (y en decimal): ' + crc_valor2 + ' (' + str(int(crc_valor2, 16)) + ')')
    valores = valores_servidor_actual.get_all()
    for i in valores:
        clave_valor = i + ':' + valores[i]
        enc_clave_valor = clave_valor.encode()
        crc_clave_valor = hex(zlib.crc32(enc_clave_valor))
        if (abs(int(crc_server_nuevo, 16)-int(crc_clave_valor, 16))) < (abs(int(crc_mi_server, 16)-int(crc_clave_valor, 16))):
            msg = 'SET ' + i + ' ' + valores[i] + '\n'
            valores_a_transferir[crc_clave_valor] = msg
    
    print('Firma server actual (y en decimal): ' + crc_mi_server + ' (' + str(int(crc_mi_server, 16)) + ')')
    print('Firma server nuevo (y en decimal): ' + crc_server_nuevo + ' (' + str(int(crc_server_nuevo, 16)) + ')')

    print('Valores antes del recalculo...')
    valores_servidor_actual.show()

    print('Valores que van al nuevo server despues del recalculo...')
    print(valores_a_transferir)