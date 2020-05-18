import socket
#Clases
from Utils.Printer import *
from ClientConfiguration import *

class BroadcastClient:

    DEFAULT_FILES_PATH  = './files/%s'
    DEFAULT_BUFFER_SIZE = 1024

    """
    Constructor
    """
    def __init__(self):
        #Socket del cliente
        self.client = None
        #Instancia de ClientConfiguration
        self.clientConfiguration = None
        #Se aplican las acciones de inicialización
        self.initialization()

    """
    Inicialización del cliente (creación y obtención del socket) 
    """
    def initialization(self):
        self.clientConfiguration = ClientConfiguration()
        self.client = self.clientConfiguration.getSocket()

    """
    Recibir los mensajes del servidor broadcast
    """
    def receiveBroadcastMessage(self):
        receivedData, addr = self.client.recvfrom(self.DEFAULT_BUFFER_SIZE)
        return receivedData

    def waitInitialSequence(self):
        self.printVerbose('Se esperará el mensaje de secuencia inicial antes de recibir las imagenes')
        #Esperamos hasta recibir el mensaje de que se va a empezar a transmitir la secuencia desde la imagen 1
        while(1):
            receivedData = self.receiveBroadcastMessage()
            decodedData = self.getDecodedData(receivedData)
            if decodedData == 'SEQUENCE_START':
                break
            else:
                Printer.printPersistentLine('La transmision ya había empezado, esperando a la siguiente transmisión')

        Printer.clear()
        self.printVerbose('Se recibió la secuencia inicial')
        return

    def getDecodedData(self, receivedData):
        decodedData = None
        try:
            decodedData = receivedData.decode('utf-8')
        except Exception:
            pass
        return decodedData

    def receiveFile(self, fileName):
        self.printVerbose('Recibiendo archivo [%s]...'%fileName)
        with open(self.DEFAULT_FILES_PATH%fileName, 'wb+') as receivedFile:
            while(1):
                receivedData = self.receiveBroadcastMessage()
                decodedData = self.getDecodedData(receivedData)

                if(decodedData == 'FILE_COMPLETE'):
                    self.printVerbose('Se recibió el archivo completo')
                    break
                #Si no se recibió el mensaje FILE_COMPLETE se sobreentiende que llegó un bloque de datos, el cual se va escribiendo en el archivo para conformarlo
                else:
                    receivedFile.write(receivedData)
        return

    def receiveContent(self):
        self.printVerbose('Recibiendo imagenes')
        #Recibimos el contenido
        while(1):
            receivedData = self.receiveBroadcastMessage()
            decodedData = receivedData.decode('utf-8')
            #Si se recibe el mensaje de que finalizó la transmisión se sale del bucle para cerrar la conexión
            if(decodedData == 'SEQUENCE_END'):
                break

            elif(decodedData.startswith('FILE_NAME')):
                fileNameHeaders = decodedData.split()
                fileName = fileNameHeaders[1]
                self.receiveFile(fileName)

            else: 
                self.printVerbose('Recibiendo contenido')

        self.printVerbose('Se recibio secuencia de término, cerrando conexión')
        print('\nSe recibieron los archivos exitosamente\n')
        return
        
    def receive(self):
        #init()
        self.waitInitialSequence()
        self.receiveContent()
    
    #Métodos que hacen referencia a los métodos de la clase ClientConfiguration
    def printVerbose(self, messageToPrint):
        self.clientConfiguration.printVerbose(messageToPrint)


def main():
    client = BroadcastClient()
    client.receive()

if __name__ == '__main__':
    main()