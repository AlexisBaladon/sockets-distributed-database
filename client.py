from clientSocket import ClientSocket
import os # Utilizado para limpiar la consola

PORT = 2022  # The port used by the server
MSG = 'GET 2022 \n' # Test message

WELCOME_MSG = ("##################################################\n"
    "#           Bienvenido a client.py CLI           #\n"
    "#                                                #\n"
    "# Redes de Computadoras - GRUPO 16               #\n"
    "#                             - Alexis Badalon   #\n"
    "#                             - Jorge Machado    #\n"
    "#                             - Mathias Martinez #\n"
    "##################################################\n\n")

MENU_OPTS = ("(1) Ejecutar metodo GET\n"
    "(2) Ejecutar metodo SET\n"
    "(3) Ejecutar metodo DEL\n"
    "(4) Ejecucion manual\n"
    "(5) Desplegar ayuda\n\n"
    "(0) Salir\n")

HELP = [("(1) Ayuda para metodo GET\n"
    "(2) Ayuda para metodo SET\n"
    "(3) Ayuda para metodo DEL\n"
    "(4) Ayuda con ejecucion manual\n\n"
    "(0) Volver al menu anterior\n"), 
    ("  Metodo GET:\nRealiza el metodo GET del Protocolo DATOS para un servidor"
    " dado. \nLa herramienta le solicitara que especifique la direccion IPv4,"
    " puerto y llave.\n")]

# Limpia la consola:
def cliClear():
    os.system('cls||clear')
    print(WELCOME_MSG)

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
                    print('SET METOD HELP\n')
                case 3:
                    cliClear()
                    print('DEL METOD HELP\n')
                case 4:
                    print('MANUAL METOD HELP\n')
                case 0:
                    return
                case _:
                    cliClear()
                    print('[ATENCION] El valor ingresado no es valido\n')
        except ValueError:
            cliClear()
            print('[ATENCION] El valor ingresado no es valido\n')

# Metodo de comunicacion con servidor mediante el Protocolo DATOS
# Precondiciones:
# - Host:Port tienen un formato valido, es decir: xxx.xxx.xxx.xxx:yyyy
# - Op es un metodo valido, GET, SET o DEL
# - Key es un string no indefinido
# - [Value] es obligatorio para el metodo SET, en cualquier otro metodo su valor
# es omitido 
def connDatos(host, port, op, key, value: str):
    # client = ClientSocket() # Gets socket
    # client.connect(client.getHost(), PORT) # Establish conection
    # client.send(MSG)
    # data = client.receive()
    # client.close()
    # print(data)
    print('xd')

def main():
    cliClear()
    while True:
        print(MENU_OPTS)
        try:
            opt = int(input('Seleccione una opcion: '))
            match opt:
                case 1:
                    cliClear()
                    print('GET METOD\n')
                case 2:
                    cliClear()
                    print('SET METOD\n')
                case 3:
                    cliClear()
                    print('DEL METOD\n')
                case 4:
                    cliClear()
                    print('MANUAL METOD\n')
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