import re
from dtServer import DtServer

#DATOS
# Estas funciones se ayudan de datos.py. para
# comunicarse con otros servers.

#Esta función determina el responsable de una key.
#La idea es que sea usada por get, set y del.
def __determine_designated_server(server: DtServer, key: str) -> tuple[str,str]:
    #retorna ip de peer
    return

#Rutina de atención tcp iniciada en descubrimiento
def client_attention_DATOS(server: DtServer, skt_client):
    return

#Parsing
def format_command_GET(method, key: str) -> str:
    #controla que termine en \n y que sea de un metodo correspondiente o retorna error
    #recibe el metodo (get set o del) y atributos y los convierte a string
    return

def format_command_SET(method, key: str, value: str) -> str:
    #controla que termine en \n y que sea de un metodo correspondiente o retorna error
    #recibe el metodo (get set o del) y atributos y los convierte a string
    return

def format_command_DEL(method, key: str, value: str) -> str:
    #controla que termine en \n y que sea de un metodo correspondiente o retorna error
    #recibe el metodo (get set o del) y atributos y los convierte a string
    return

def parse_command_GET(command: str) -> str:
    num_command = re.sub(r"\D", "", command)
    return num_command

def parse_command_SET(command: str) -> tuple[str,str]:
    num_command = re.findall(r'\d', command)
    return num_command

def parse_command_DEL(command: str) -> str:
    num_command = re.sub(r"\D", "", command)
    return num_command

if __name__ == "__main__":
    #asddas
    command = "GET 1234 \n"
    print(parse_command_GET(command))
    command = "SET 1234 sdfsdf3242234 \n"
    print(parse_command_GET(command))
    command = "DEL 124 \n"
    print(parse_command_GET(command))