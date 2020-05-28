import socket
#Clases
from ServerConfiguration import *
from FileManager import *


class BroadcastServer:

    FILES_PATH = './files/%s'

    def __init__(self):
        #Socket
        self.server = None
        #ServerConfiguration instance
        self.serverConfiguration = None
        #Broadcast address
        self.broadcastAddress = None
        #Current FileManager instance
        self.fileManager = None
        #Inicialización
        self.initialization()

    def initialization(self):
        self.serverConfiguration = ServerConfiguration()
        self.server = self.serverConfiguration.getSocket()
        self.broadcastAddress = self.serverConfiguration.getBroadcastAddress()
    

    def sendMessage(self, message):
        if(type(message) != bytes):
            message = message.encode('utf-8')
        self.server.sendto(message, (self.broadcastAddress, 37020))
        return

    def sendInitialSequenceMessage(self):
        self.sendMessage('SEQUENCE_START')
        self.printVerbose('########################################')
        self.printVerbose('\nSe envia mensaje de inicio de secuencia\n')
        return

    def sendFinalSequence(self):
        self.sendMessage('SEQUENCE_END')
        print('Secuencia enviada exitosamente')
        self.printVerbose('\nSe envia mensaje de término de secuencia\n')
        return

    def printContentToSend(self):
        self.printVerbose('\nImagenes a enviar: \n%s'%str(self.getFilesToSend()))
        self.printVerbose('\nInicio del envio de las imagenes')
        return

    def processFile(self, fileToSend):
        self.fileManager = FileManager(fileToSend, self.FILES_PATH%fileToSend)
        self.fileManager.processFile()


    def sendFileBytesByBlocks(self):
        while(1):
            #Vamos extrayendo los bytes del archivo (con un tamaño de 1024 en cada iteración)
            fileBytes = self.fileManager.getFileBytes()
            #Si llegamos al fin del archivo salimos del bucle
            if(not fileBytes):
                break
            self.sendMessage(fileBytes)
        return

    def sendFile(self, fileToSend):
        self.printVerbose('\t\nENVIANDO ARCHIVO = [%s]'%fileToSend)
        self.processFile(fileToSend)
        self.sendMessage('FILE_NAME %s'%fileToSend)
        self.sendFileBytesByBlocks()
        self.sendMessage('FILE_COMPLETE')
        self.fileManager.closeFile()
        self.wait(1)

    
    def sendContent(self):
        filesToSend = self.getFilesToSend()
        #Enviamos las imágenes
        for fileToSend in filesToSend:
            self.sendFile(fileToSend)
        #Informamos en la console que terminó el envío de imágenes
        self.printVerbose('Fin del envio de las imagenes\n')
        return

    def transmit(self):
        self.sendInitialSequenceMessage()
        self.printContentToSend()
        self.sendContent()
        self.sendFinalSequence()
        self.wait()
        return
    
    #Métodos que hacen referencia a los métodos de la clase ServerConfiguration
    def printVerbose(self, messageToPrint):
        self.serverConfiguration.printVerbose(messageToPrint)
    
    def wait(self, seconds = None):
        self.serverConfiguration.wait(seconds)
    
    def getFilesToSend(self):
        return self.serverConfiguration.getFilesToSend()



def main():
    server = BroadcastServer()
    while True:
        server.transmit()

if __name__ == "__main__":
    main()