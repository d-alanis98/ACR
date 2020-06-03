import json
import tftpy
from os import system, path

#CONSTANTES

#Nombre de llave que contiene el array de routers
ROUTERS = 'routers'
#Propiedades del cada entrada de la lista de routers
NAME = 'name'
ADDRESS = 'address'
FILE_NAME = 'fileName'
#Puerto del servidor TFTP
TFTP_PORT = 69
#Directorio que contendrá los resultados
ROUTERS_ROOT_DIRECTORY = 'Routers'
#Comandos de sistema operativo
FIND_ROOT_DIRECTORY = './%s' % ROUTERS_ROOT_DIRECTORY
CREATE_ROOT_DIRECTORY = 'mkdir %s' % ROUTERS_ROOT_DIRECTORY
ROUTER_DIRECTORY_COMMAND = 'mkdir Routers/%s'
MOVE_ROUTER_FILE_COMMAND = 'mv %s Routers/%s'


#Lista de routers extraidos de archivo de configuración
routers = []

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

'''
Obtiene el archivo de configuración del servidor TFTP del router 
'''   
def getTFTPFile(router):
    fileName = router[FILE_NAME] #Obtiene el nombre del archivo de configuración del router mediante su llave filename
    tftpServerAddress = router[ADDRESS] #Obtiene la dirección del servidor TFTP del router mediante su llave address
    print('Obteniendo archivo %s desde el servidor TFTP [%s:%d]' % (fileName, tftpServerAddress, TFTP_PORT))
    client = tftpy.TftpClient(tftpServerAddress, TFTP_PORT) 
    client.download(fileName, fileName)
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
        getTFTPFile(router)
        moveFileToRouterFolder(router)

#MAIN
def main():
    initialization()
    getRoutersFiles()

if __name__ == '__main__':
    main()    
