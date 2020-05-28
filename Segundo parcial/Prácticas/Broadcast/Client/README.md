# BroadcastClient
Cliente para la recepción de los archivos transmitidos por el servidor broadcast.
## Modo de uso
```
python ./BroadcastClient.py [-v] [--help]
```
### Options
	- [-v]
		Verbose. Imprime todos los mensajes que indican el estado del cliente en la terminal.
	- [--help]
		Imprime el modo de uso de este programa, así como sus opciones disponibles.
#### Troubleshooting
Si llegara a presentarse un error `Utils is not a module`, ejecutar el siguiente comando en el directorio Client:
```
export PYTHONPATH=$PYTHONPATH:`pwd`
```
