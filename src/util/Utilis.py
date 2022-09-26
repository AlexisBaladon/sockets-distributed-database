## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo de Utilidades (Utilis.py) ##

# Definicion de Imports #
import ipaddress # Utilizado para checkear direcciones IPv4
from src.exceptions.KeyError import KeyError
from src.exceptions.MethodError import MethodError

# Definicion de Constantes #
METHODS = ['GET', 'SET', 'DEL']
CHARS_TO_FILTER = [" ", "\n", "\r", "\t"]

# Checkea si 'addr' es una direccion IPv4 valida
def checkIp(addr: str) -> bool:
    res = False
    try:
        ip = ipaddress.ip_address(addr)
        if (ip.version == 4):
            res = True
    except ValueError:
        pass
    return res

# Checkea si 'input' NO contiene espacios o caracteres especiales como:
#   "\n", "\r", "\t"
def checkStr(value: str) -> bool:
    print(value)
    for spChar in CHARS_TO_FILTER:
            if spChar in value:
                return False
    return True

# Genera el mensaje a enviar siguiendo el prtocolo DATOS
# En caso de que el mensaje no cumpla con el protocolo, se genera una
#   excepcion acorde, tales como:
# - MethodError: Ocurre cuando el metodo indicado no es soportado por DATOS
# - KeyError: Ocurre cuando la key contiene caracteres especiales como espacios,
#   "\n", "\r" o "\t"; o es vacio
# - ValueError: Ocurre cuando el valor contiene caracteres especiales como 
#   espacios, "\n", "\r" o "\t"; o es vacio
def genMsgDatos(method: str, key: str, value: str) -> str:
    message = method.upper()
    if message in METHODS:
        if (checkStr(key) and not key == ''):
            message += ' ' + key
            if (method == 'SET'):
                if (checkStr(value) and not value == ''):
                    message += ' ' + value
                else:
                    raise ValueError("El valor %s ingresado no es valido" % value)
            return message + '\n'
        else:
            raise KeyError("La key %s ingresada no es valida" % key)
    else:
        raise MethodError("Metodo %s no soportado" % method)