#!/usr/bin/python

## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Cliente (client.py) ##

# Definicion de Imports #
import sys, getopt
from src.client.clientSocket import getLocalhost, sendMsgDatos
from src.util.utilis import checkIp, checkPort, genMsgDatos, parseCommand

# Definicion de Constantes #
HELP = ["client.py [options] | <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n",
    (" ServerIP:        Dirección IP del servidor al que se desea conectar\n"
    "  ServerPort:      Puerto del servidor al que se desea conectar\n"
    "  Op:              Operación a realizar: GET, SET o DEL\n"
    "  Key:             Clave del valor que se desea leer, escribir o borrar\n"
    "  Value:           Valor a almacenar. Solo al usar metodo SET\n\n"
    "Options:\n  -h:    Imprime el texto de ayuda")]

# Definicion de Funciones #

# Metodo de comunicacion con servidor mediante el Protocolo DATOS
# Precondiciones:
# - Host:Port tienen un formato valido, es decir: xxx.xxx.xxx.xxx:yyyy
# - Msg es un mensaje valido para el Protocolo DATOS
def connDatos(addr: str, port: str, msg: str):
    print('\nSumario:')
    print('*Conexion: %s:%d\n' % (addr, port))
    print('*Mensaje enviado: %s' % msg)
    try:
        data = sendMsgDatos(addr, port, msg)
        print('*Respuesta obtenida: %s' % data)
    except TimeoutError as te:
        print('[TIMEOUT_ERR] ' + str(te))
    except InterruptedError as ie:
        print('[INTERRUPTED_ERR] ' + str(ie))
    except Exception as e:
        print('[ERR] ' + str(e))
    return None

# Funcion principal, ejecuta la logica de cliente para los argumentos ingresados
#   en la invocacion. Utilizada por clientCLI.py para "MetodoManual"
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"h")
    except getopt.GetoptError:
        print(HELP[0])
        return None
    if (('-h', '') in opts):
        print(HELP[0], HELP[1])
        return None
    if (len(args) > 5):
        print("[ATENCION] Demasiados argumentos")
        print(HELP[0])
        return None
    elif (len(args) < 4):
        print("[ATENCION] Argumentos faltantes")
        print(HELP[0])
        return None
    elif (len(args) == 4): # Seteo value como el string vacio, si no existe
        args.append('')
    if (args[0] == 'localhost'):
            args[0] = getLocalhost()
    try:
        mensaje = genMsgDatos(args[2], args[3], args[4])
        if (parseCommand(mensaje)[0] == None):
            print("[ATENCION] Formato de mensaje invalido")
            print(HELP[0])
            return None
        connDatos(checkIp(args[0]), checkPort(args[1]), mensaje)
    except Exception as e:
        print("[ATENCION] ", str(e))
        print(HELP[0])
    return None

# Main Init #
if __name__ == "__main__":
    main(sys.argv[1:])