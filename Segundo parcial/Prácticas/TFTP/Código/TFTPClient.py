import json
import tftpy
from os import system, path
from RouterTelnetClient import RouterTelnetClient

#CONSTANTES

#Nombre de llave que contiene el array de routers
ROUTERS = 'routers'
#Propiedades del cada entrada de la lista de routers
NAME = 'name'
ADDRESS = 'address'
FILE_NAME = 'fileName'
#Parámetros de la comunicación Telnet
TELNET_USER = 'telnetUser'
TELNET_PASSWORD = 'telnetPassword'
#Parámetros del servidor TFTP (en el host, sin embargo, no se pone localhost por si se desea ejecutar este script desde otro cliente en la topología)
TFTP_PORT = 69
TFTP_SERVER_ADDRESS = '10.10.2.4'
#Directorio que contendrá los resultados
ROUTERS_ROOT_DIRECTORY = 'Routers'
#Comandos de sistema operativo
FIND_ROOT_DIRECTORY = './%s' % ROUTERS_ROOT_DIRECTORY
CREATE_ROOT_DIRECTORY = 'mkdir %s' % ROUTERS_ROOT_DIRECTORY
ROUTER_DIRECTORY_COMMAND = 'mkdir Routers/%s'
MOVE_ROUTER_FILE_COMMAND = 'mv %s Routers/%s'


#Lista de routers extraidos de archivo de configuración
routers = []

telnetConnection = None

#FUNCIONES
'''
Comprueba si el directorio que contiene los resultados existe
'''
def resultsDirectoryExists():
    return path.exists(FIND_ROOT_DIRECTORY)

'''
Crea el directorio que contendrá las carpetas con cada archivo de configuración de cada router
'''
def createBaseDirectory():
    system(CREATE_ROOT_DIRECTORY)
    return

'''
Inicializa la lista de routers con los datos extraidos del archivo de configuración
'''
def setRouters():
    global routers 
    routers = getRoutersFromFile()
    return

'''
Obtiene cada entrada o item de la lista de routers desde ek archivo de configuración
'''
def getRoutersFromFile():
    routersNames = []
    with open('conf.json') as configurationFile:
        options = json.load(configurationFile) #Lo carga como JSON para poder acceder a sus propiedades
        for router in options[ROUTERS]: #Iteramos sobre los items que contiene el array de la llave ROUTERS (routers)
            routersNames.append(router) #Agregamos cada item a la lista temporal (no mutamos la lista global para que esta sea una función pura, sin efectos colaterales)
    return routersNames

'''
Se crea un directorio para contener el archivo de configuración de cada router, este es creado con el mismo nombre con el que se declaró 
en la llave name del archivo de configuración para cada router
'''
def createRoutersDirectories():
    global routers
    for router in routers:
        print('Se creara directorio %s' % router[NAME])
        system(ROUTER_DIRECTORY_COMMAND % router[NAME])
    return

'''
Función para inicializar la lista de routers y crear los directorios si estos no existían
'''
def initialization():
    setRouters()
    if(not resultsDirectoryExists()):
        createBaseDirectory()
        createRoutersDirectories()
    return


def setTelnetConnectionCredentials(router, telnetConnection):
    user = router[TELNET_USER]
    password = router[TELNET_PASSWORD]
    telnetConnection.setTelnetClientCredentials(user, password)

def initTelnetCommunication(router):
    global telnetConnection
    routerAddress = router[ADDRESS] #Obtiene la dirección del servidor TFTP del router mediante su llave address
    outputFileName = router[FILE_NAME]
    telnetConnection = RouterTelnetClient(routerAddress, outputFileName)
    setTelnetConnectionCredentials(router, telnetConnection)

def backupRouterFileInTFTPServer(router):
    global telnetConnection
    telnetConnection.executeBackup()

'''
Obtiene el archivo de configuración del servidor TFTP del router 
'''   
def getTFTPFile(router):
    fileName = router[FILE_NAME] #Obtiene el nombre del archivo de configuración del router mediante su llave filename
    print('Obteniendo archivo %s desde el servidor TFTP [%s:%d]' % (fileName, TFTP_SERVER_ADDRESS, TFTP_PORT))
    client = tftpy.TftpClient(TFTP_SERVER_ADDRESS, TFTP_PORT) 
    client.download(fileName, fileName)
    print('Archivo %s obtenido exitosamente!' % fileName)
    return

'''
Mueve el archivo del pwd actual a la carpeta específica para ese router
'''
def moveFileToRouterFolder(router):
    system(MOVE_ROUTER_FILE_COMMAND % (router[FILE_NAME], router[NAME]))
    return

'''
Obtiene el archivo de configuración de cada router y lo coloca en su correspondiente carpeta
'''
def getRoutersFiles():
    global routers
    for router in routers:
        initTelnetCommunication(router)
        backupRouterFileInTFTPServer(router)
        getTFTPFile(router)
        moveFileToRouterFolder(router)

#MAIN
def main():
    initialization()
    getRoutersFiles()

if __name__ == '__main__':
    main()    
