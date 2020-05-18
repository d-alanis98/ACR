# BroadcastServer
Servidor que envía paquetes por multidifusión o broadcast, los cuales contienen a los bloques que conforman los archivos incluidos en el directorio files/, los cuales son reconstruidos por el cliente al ser recibidos.

## Modo de uso 
```
python3 BroadcastServer.py [-v] [-t seconds] [--help]
```
### Options
	- [-v]
		Verbose. Imprime todos los mensajes que indican el estado del servidor en la terminal.
	- [-t seconds]
		Modifica el timeout o la cantidad de segundos que se espera entre cada retransmisión, por defecto son 2 segundos.
	- [--help]
		Imprime el modo de uso de este programa, así como sus opciones disponibles.
 
