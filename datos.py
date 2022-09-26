import re
import zlib
from dtServer import DtServer

ERROR_MSG = "NO\n"

#DATOS
# Estas funciones se ayudan de datos.py. para
# comunicarse con otros servers.

#Esta función determina el responsable de una key.
#La idea es que sea usada por get, set y del.
def determine_designated_server(server: DtServer, key: str) -> tuple[str,str]:
    key_crc = zlib.crc32(key)
    min_distance = abs(server.firma - key_crc)
    min_socket = server.socket #FALTA
    
    for peer_key in server.peers:
        peer = server.peers[peer_key]
        peer_distance = abs(peer.crc - key_crc)
        if peer_distance < min_distance:
            min_distance = peer_distance
            min_socket = peer.socket #FALTA

    return min_socket

#Rutina de atención tcp iniciada en descubrimiento
#THREAD
def client_attention_DATOS(server: DtServer, skt_client):
    database_access = {
        "GET": lambda x, y: server.database.get(x),
        "SET": server.database.set,
        "DEL": lambda x, y: server.database.delete(x),
    }

    while True:
        response = ERROR_MSG
        query = skt_client.receive() #bloqueante. Aun no se como llega el receive
        method, key, value = parse_command(query)
        if method is not None:
            owner_socket = determine_designated_server(key)
            if owner_socket == server.socket:
                response = database_access[method](key, value) #ojo con return
                response = format_response(method, response)
            else:
                formated_msg = format_method(method, key, value)
                #adquirir
                peer_skt.send(formated_msg) #Ciclos?
                response = peer_skt.receive()
                #soltar

        skt_client.send(response) #falta
                #variable de 'enuso' y lock. Lock debe ser realizado por server (desconexiones!!)
            #for peer_key in server.peers:
            #    peer_ip = server.peers[key].ip
            #    peer_port = server.peers[key].port
            #    if peer_ip == owner_ip and peer_port == owner_port:
            #        peer_socket = server.peers[key].socket #ups no me di cuenta de esto

    skt_client.close() #OJO AL PIOJO
    return

def format_response(method, response):
    if response == None:
        return "NO\n"
    if method == "GET":
        return f'OK {response}\n'
    return 'OK\n'

#Parsing

def format_method(method:str, key: str, value: str = "") -> str:
    if method == "SET":
        return f'{method} {key} {value}\n'
    return f'{method} {key}\n'

#Devuelve el metodo o None en caso de tener un formato erróneo
def parse_command(command: str) -> tuple[str,str,str]:
    regex_methods = {
        "GET": r'^GET (\d|\w+)\n$',
        "SET": r'^SET (\d|\w+) (\d|\w+)\n$',
        "DEL": r'^DEL (\d|\w+)\n$'
    }

    for method in regex_methods:
        regex = re.compile(regex_methods[method])
        method_match = regex.match(command)
        if method_match is not None:
            key = method_match.group(1)
            value = method_match.group(2) if method == "SET" else None
            return method, key, value

    return None, None, None

if __name__ == "__main__":
    right_get = "GET 123a111\n"
    right_set = "SET 123a1 1abc\n"
    right_del = "DEL 123b111a\n"
    wrong_msg = "GET 123/abc\n"

    #import zlib
    #print(zlib.crc32(b"holaquetal"))
    #print(format_method('GET','12',None))
    parsed1, parsed2, parsed3 = parse_command(right_get)
    print(parsed1, parsed2, parsed3)
    parsed1, parsed2, parsed3 = parse_command(right_set)
    print(parsed1, parsed2, parsed3)
    parsed1, parsed2, parsed3 = parse_command(right_del)
    print(parsed1, parsed2, parsed3)
    parsed1, parsed2, parsed3 = parse_command(wrong_msg)
    print(parsed1, parsed2, parsed3)
    #met = get_method("GET 123\n")
    #print(met)
    #met = get_method("SET 123 123\n")
    #print(met)
    #met = get_method("DEL 123\n")
    #print(met)

    #command = "GET 1234 \n"
    #print(parse_command_GET(command))
    #command = "SET 1234 sdfsdf3242234 \n"
    #print(parse_command_GET(command))
    #command = "DEL 124 \n"
    #print(parse_command_GET(command))
    #command = "ANNOUNCE 124 \n"