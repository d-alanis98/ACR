from telnetlib import Telnet
from getpass import getpass
import sys

class TelnetClient:
    DEFAULT_PORT = 23
    def __init__(self, host, port = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.user = None
        self.password = None
        self.telnetInstance = None

    def areCredentialsSet(self):
        return self.user and self.password
    
    def setCredentials(self, user, password):
        self.user = user
        self.password = password

    def requestCredentials(self):
        self.user = input('Ingrese usuario de [%s]: ' % self.host)
        self.password = getpass()

    def connect(self):
        #Si aún no se han establecido solicitamos las credenciales (nombre de usuario y contraseña)
        if not self.areCredentialsSet():
            self.requestCredentials()
        #Creamos una instancia de Telnet
        self.telnetInstance = Telnet(self.host)
        #Leemos todo el flujo de bytes hasta encontrar el mensaje Username: (solicitando que se ingrese)
        self.readUntil('Username: ')
        #Escribimos el nombre de usuario codificado en ascii
        self.executeCommand(self.user)
        #self.telnetInstance.write(self.user.encode('ascii') + b"\n")
        if self.password:
            self.readUntil('Password: ')
            #self.telnetInstance.write(self.password.encode('ascii') + b'\n')
            self.executeCommand(self.password)
            return True
        return False
    
    def executeCommand(self, command):
        commandWithLineBreak = '%s\n' % command
        self.telnetInstance.write(bytes(commandWithLineBreak, 'ascii'))
    
    def readUntil(self, target):
        self.telnetInstance.read_until(target.encode('ascii'))
    
    def write(self, message):
        self.telnetInstance.write(bytes(message, 'ascii'))

    def interact(self):
        self.telnetInstance.interact()

    def printSession(self):
        print(self.telnetInstance.read_all().decode('ascii'))


