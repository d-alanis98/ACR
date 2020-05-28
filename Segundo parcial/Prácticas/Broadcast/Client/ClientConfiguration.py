import sys
import socket

class ClientConfiguration:
    def __init__(self):
        self.verbose = False
        self.serverIp = '0.0.0.0'
        self.clientSocket = None
        self.initialization() #Corremos la configuración inicial

    def printVerbose(self, messageToPrint):
        if self.verbose:
            print(messageToPrint),
        return

    def getSocket(self):
        return self.clientSocket

    def exitProgram(self, status = 1):
        exit(status)

    def printUseMode(self):
        print('\nModo de uso: python3 BroadcastClient.py [-v]  \n')

    def printHelp(self):
        print('[-v]: Modo verbose, se mouestran las impresiones de las acciones generadas\n')


    def getArguments(self):
        global serverIp
        for index, arg in enumerate(sys.argv[1:]):
            if(arg == '-h'):
                self.printUseMode()
                self.printHelp()
                self.exitProgram(0)
            elif(arg == '-v'):
                self.verbose = True
            else:
                self.printUseMode()
                self.exitProgram()
        return

    def initialization(self):
        self.getArguments()
        #Creamos el socket
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        # Establecemos la operación de SO_REUSEPORT, para poder reutilizar puertos y tener un solo (host, port). 
        self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # Habilitamos broadcast
        self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #Enlazamos el socket
        self.clientSocket.bind((self.serverIp, 37020))
    
