#!/usr/bin/python

import sys, getopt

HELP = ["client.py [options] | <ServerIP> <ServerPort> <Op> <Key> [<Value>]\n",
    (" ServerIP:        Dirección IP del servidor al que se desea conectar\n"
    "  ServerPort:      Puerto del servidor al que se desea conectar\n"
    "  Op:              Operación a realizar: GET, SET o DEL\n"
    "  Key:             Clave del valor que se desea leer, escribir o borrar\n"
    "  Value:           Valor a almacenar. Solo al usar metodo SET\n\n"
    "Options:\n  -h:    Imprime el texto de ayuda")]

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"ht:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(HELP[0])
        sys.exit(2)
    print(str(opts))
    print(str(args))
    for opt, arg in opts:
        if opt == '-h':
            print(HELP[0], HELP[1])
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print ('Input file is "', inputfile)
    print ('Output file is "', outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])