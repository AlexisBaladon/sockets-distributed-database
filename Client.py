## Redes de Computadoras 2022 - Facultad de Ingenieria - UdelaR
## GRUPO 16:
##   - Alexis Badalon
##   - Jorge Machado
##   - Mathias Martinez

## Modulo Principal de Cliente (Client.py) ##

# Definicion de Imports #
import os # Utilizado para limpiar la consola
from src.client.ClientSocket import sendMsgDatos
from src.client.ClientSocket import getLocalhost
from src.util.Utilis import checkIp 
from src.util.Utilis import genMsgDatos 

# Definicion de Constantes #
METHODS = ['GET', 'SET', 'DEL']
WELCOME_MSG = ("##################################################\n"
    "#           Bienvenido a client.py CLI           #\n"
    "#                                                #\n"
    "# Redes de Computadoras - GRUPO 16               #\n"
    "#                             - Alexis Badalon   #\n"
    "#                             - Jorge Machado    #\n"
    "#                             - Mathias Martinez #\n"
    "##################################################\n")
MENU_OPTS = ("(1) Ejecutar metodo GET\n"
    "(2) Ejecutar metodo SET\n"
    "(3) Ejecutar metodo DEL\n"
    "(4) Ejecucion manual\n"
    "(5) Desplegar ayuda\n\n"
    "(0) Salir\n")
HELP = [("(1) Ayuda para metodo GET\n(2) Ayuda para metodo SET\n"
    "(3) Ayuda para metodo DEL\n(4) Ayuda con ejecucion manual\n\n"
    "(0) Volver al menu anterior\n"), 
    ("  Metodo GET:\nRealiza el metodo GET del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto y llave.\n"), 
    ("  Metodo SET:\nRealiza el metodo SET del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto, llave y valor.\n"), 
    ("  Metodo DEL:\nRealiza el metodo DEL del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto y llave.\n"), 
    ("  Ejecucion Manual:\nPermite la ejecucion manual de operaciones mediante"
    " el Protocolo DATOS.\nEl metodo de invocacion viene dado por:\n"
    "    <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n")]

# Limpia la consola:
def cliClear():
    os.system('cls||clear')
    print(WELCOME_MSG)

# Imprime el texto de ayuda
def help():
    cliClear()
    while True:
        print(HELP[0])
        try:
            opt = int(input('Seleccione una opcion: '))
            match opt:
                case 1:
                    cliClear()
                    print(HELP[1])
                    input("Presione ENTER para volver al menu principal... ")
                    return
                case 2:
                    cliClear()
                    print(HELP[2])
                    input("Presione ENTER para volver al menu principal... ")
                    return
                case 3:
                    cliClear()
                    print(HELP[3])
                    input("Presione ENTER para volver al menu principal... ")
                    return
                case 4:
                    cliClear()
                    print(HELP[4])
                    input("Presione ENTER para volver al menu principal... ")
                    return
                case 0:
                    return
                case _:
                    cliClear()
                    print('[ATENCION] El valor ingresado no es valido\n')
        except ValueError:
            cliClear()
            print('[ATENCION] El valor ingresado no es valido\n')

# Obtiene la direccion a enviar de la entrada de la tabla
def inputAddr():
    cliClear()
    print('Obteniendo direccion a conectar')
    addr = getLocalhost()
    while True:
        addr = input("Ingrese direccion del servidor: ")
        if (addr == '' or addr == 'localhost'):
            addr = getLocalhost()
            break
        else:
            if (checkIp(addr)):
                break
            else:
                print('[ATENCION] Por favor, ingrese una direccion valida\n')
    port = 2022
    while True:
        try:
            port = int(input("Ingrese puerto a conectarse: "))
            if (port >= 0 and port <= 65535):
                break
            else:
                print('[ATENCION] Por favor, ingrese un puerto valido\n')
        except ValueError:
            print('[ATENCION] Por favor, ingrese un puerto valido\n')
    return (addr, port)

# Genera los datos necesarios para enviar un mensaje mediante el protocolo DATOS
# Lee la entrada provista por el usuario
# Retorna la tupla (addr, port, message), donde:
# -addr es la direccion IPv4 del servidor
# -port es el puerto del servidor
# -message es el mensaje a ser enviado
def inputMethodAuto(method: str) -> str:
    cliClear()
    print('Generando mensaje con el metodo %s\n' % method)
    key = ''
    while True:
        key = input('Ingrese clave: ')
        if (not key == ''):
            break
        else:
            print('[ATENCION] Por favor, ingrese una clave valida\n')
    value = ''
    if method.upper() in METHODS:
        while True:
            value = input('Ingrese valor: ')
            if (not value == ''):
                break
            else:
                print('[ATENCION] Por favor, ingrese un valor valido\n')
    msg = ''
    try:
        msg = genMsgDatos(method, key, value)
    except Exception as e:
        print('[ERR] ' + str(e))
    return msg

def manualInput() -> str:
    cliClear()
    print('Opcion deshabilitada por el momento, favor comprender...')
    print('Pruebe utilizar las funciones automaticas')
    input('Pesione ENTER para volver al menu principal...')
    return ''

# Metodo de comunicacion con servidor mediante el Protocolo DATOS
# Precondiciones:
# - Host:Port tienen un formato valido, es decir: xxx.xxx.xxx.xxx:yyyy
# - Msg es un mensaje valido para el Protocolo DATOS
def connDatos(addr: str, port: str, msg: str):
    cliClear()
    try:
        data = sendMsgDatos(addr, port, msg)
        print('\nSumario:')
        print('*Conexion: %s:%d' % (addr, port))
        print('*Mensaje enviado: %s' % msg)
        print('*Respuesta obtenida: %s' % data)
        input('Operacion completada, presione ENTER para continuar!')
    except TimeoutError as te:
        print('[TIMEOUT_ERR] ' + str(te))
    except InterruptedError as ie:
        print('[INTERRUPTED_ERR] ' + str(ie))
    except Exception as e:
        print('[ERR] ' + str(e))

def main():
    cliClear()
    while True:
        print(MENU_OPTS)
        try:
            opt = int(input('Seleccione una opcion: '))
            match opt:
                case 1:
                    (addr, port) = inputAddr()
                    msg = inputMethodAuto("GET")
                    connDatos(addr, port, msg)
                    cliClear()
                case 2:
                    (addr, port) = inputAddr()
                    msg = inputMethodAuto("SET")
                    connDatos(addr, port, msg)
                    cliClear()
                case 3:
                    (addr, port) = inputAddr()
                    msg = inputMethodAuto("DEL")
                    connDatos(addr, port, msg)
                    cliClear()
                case 4:
                    manualInput()
                    cliClear()
                case 5:
                    help()
                    cliClear()
                case 0:
                    print('Finalizando...')
                    break
                case _:
                    cliClear()
                    print('[ATENCION] El valor ingresado no es valido\n')
        except ValueError:
            cliClear()
            print('[ATENCION] El valor ingresado no es valido\n')

# Main Init
if __name__ == "__main__":
    main()
