import sys
import time
import socket
from os import listdir
from os.path import isfile, join

class ServerConfiguration:
    def __init__(self):
        #Socket
        self.serverSocket = None
        #Opciones internas habilitables mediante linea de comandos
        self.verbose = False
        self.cacheFileNames = True
        self.transmisionInterval = 1
        #Listado de archivos a enviar
        self.filesToSend = None
        #Acciones de inicialización
        self.initialization()

    def getSocket(self):
        return self.serverSocket

    
    def printVerbose(self, messageToPrint):
        if self.verbose:
            print(messageToPrint)
        return
    
    def wait(self, seconds = None):
        seconds = seconds or self.transmisionInterval
        time.sleep(seconds)

    def exitProgram(self, status = 1):
        exit(status)

    def printUseMode(self):
        print('\nModo de uso: python3 BroadcastServer.py [-v] [-t numeroSegundos] [--no-cache]\n')

    def printHelp(self):
        print('[-v]: Modo verbose, se mouestran las impresiones de las acciones generadas\n')
        print('[-t segundos]: Se modificará el tiempo de espera entre cada retransmisión (default: 1s)\n')
        print('[--no-cache]: Se escanearán los archivos en el directorio en cada transmisión\n')

    def getArguments(self):
        for index, arg in enumerate(sys.argv[1:]):
            if(arg == '-h'):
                self.printUseMode()
                self.printHelp()
                self.exitProgram(0)
            if(arg == '-v'):
                self.verbose = True
            if(arg == '--no-cache'):
                self.cacheFileNames = False
            if(arg == '-t'): 
                index += 2
                if len(sys.argv) <= index:
                    self.printUseMode()
                    self.exitProgram()
                self.transmisionInterval = float(sys.argv[index])
        return

    def setFilesToSend(self):
        #Comprobamos si es necesario obtener los archivos (la primera vez siempre es necesario pues self.filesToSend es nulo)
        if(self.filesToSend and self.cacheFileNames): #Si la bandera --no-cache fue introducida cacheFileNames será False y siempre se estará obteniendo el listado de archivos
            return
        filesPath = './files'
        self.filesToSend = [f for f in listdir(filesPath) if isfile(join(filesPath, f))]

    def getFilesToSend(self):
        if self.filesToSend == None:
            self.setFilesToSend()
        return self.filesToSend

    def initialization(self):
        #Obtenemos los argumentos de la línea de comandos
        self.getArguments()
        #Socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Establecemos la operación de SO_REUSEPOR, para poder reutilizar puertos y tener un solo (host, port). 
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # Habilitamos el modo broadcast
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Timeout para que el socketno se bloqueé al recibir datos
        self.serverSocket.settimeout(5)
        return
