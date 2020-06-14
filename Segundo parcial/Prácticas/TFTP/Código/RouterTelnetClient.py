from getpass import getpass
from TelnetClient import TelnetClient


class RouterTelnetClient:
    #Constantes
    EXIT                        = 'exit'
    ENTER                       = '\n'
    ENABLE                      = 'en'
    PASSWORD                    = 'Password: '
    ROUTER_FILE_NAME            = 'start'
    ENTER_ENABLE_PASSWORD       = 'Introduzca contraseña de enable del router'
    TFTP_SERVER_ADDRESS         = '10.10.2.4'
    COPY_FILE_TO_TFTP_SERVER    = 'copy %s tftp://%s' % (ROUTER_FILE_NAME, TFTP_SERVER_ADDRESS)
    CONFIRMATION_END_OF_LINE    = '? '

    def __init__(self, routerAddress, outputFileName):
        self.routerAddress = routerAddress
        self.outputFileName = outputFileName
        self.enablePassword = None
        self.telnetClientInstance = None
        #Establecemos la instancia del cliente telnet
        self.setTelnetClientInstance()
    
    """
    Establece la instancia del cliente telnet con la que se gestionará la conexión al router, mediante una instancia de la clase TelnetClient
    """
    def setTelnetClientInstance(self):
        self.telnetClientInstance = TelnetClient(self.routerAddress)

    """
    Establece las credenciales de telnet del router (para que no se tengan que ingresar manualmente)
    """
    def setTelnetClientCredentials(self, user, password):
        self.telnetClientInstance.setCredentials(user, password)

    """
    Se conecta por telnet al router por medio del método connect de la clase TelnetClient
    """
    def connect(self):
        return self.telnetClientInstance.connect()

    """
    Copia el archivo startup-config del router al servidor TFTP
    """
    def copyRouterFileToTFTP(self):
        telnetClient = self.telnetClientInstance
        telnetClient.executeCommand(self.COPY_FILE_TO_TFTP_SERVER)
        telnetClient.readUntil(self.CONFIRMATION_END_OF_LINE)
        telnetClient.write(self.ENTER)
        telnetClient.readUntil(self.CONFIRMATION_END_OF_LINE)
        print('Guardando archivo %s en servidor TFTP' % self.outputFileName)
        telnetClient.executeCommand(self.outputFileName)
    """
    Termina la sesión telnet
    """
    def exitSession(self):
        telnetClient = self.telnetClientInstance
        telnetClient.executeCommand(self.EXIT)
    """
    Realiza el backup del archivo startup-config del router en el servidor TFTP, gestionando todas las acciones necesarias
    desde la conexión hasta la entrada a la zona privilegiada y la copia del archivo en cuestión
    """
    def executeBackup(self):
        if self.connect():
            self.copyRouterFileToTFTP()
            self.exitSession()
