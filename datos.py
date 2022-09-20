

#DATOS
# Estas funciones se ayudan de datos.py. para
# comunicarse con otros servers.

#Esta función determina el responsable de una key.
#La idea es que sea usada por get, set y del.
def __determine_designated_server(key: str) -> tuple[str,str]:
    #retorna ip de peer
    return

#Rutina de atención tcp iniciada en descubrimiento
def client_attention_DATOS(self, skt_client):
    return

#Parsing
def format_command_DATOS(method, key: str, value: str = "") -> str:
    #controla que termine en \n y que sea de un metodo correspondiente o retorna error
    #recibe el metodo (get set o del) y atributos y los convierte a string
    return

def parse_command_GET(command: str) -> tuple[str,str,str]:
    return

def parse_command_SET(command: str) -> tuple[str,str,str]:
    return

def parse_command_DEL(command: str) -> tuple[str,str,str]:
    return