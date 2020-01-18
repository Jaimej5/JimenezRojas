## SISTEMAS DISTRIBUIDOS 2019/20: PRÁCTICA
https://github.com/Jaimej5/JimenezRojas

## INTEGRANTES
* Jaime Jiménez Catalán
* Álvaro Rojas Parra

## RAMAS DEL REPOSITORIO

| *Entrega*        | *Rama*          |
| ------------- |:-------------:|
| Entrega 1     | L1 |
| Entrega 2      | L2      |
| Entrega 3 | L3      |

## ENUNCIADO
El objetivo principal del proyecto contenido en este repositorio es diseñar un sistema cliente-servidor 
que permita la descarga de ficheros a partir de URIs. El ejemplo típico será la descarga de clips de audio
de YouTube.

Para implementar el sistema se llevaran a cabo tres fases:
* **FASE 1(L1)**: Introducción de los Actores
* **FASE 2(L2)**: Descarga y sincronización de componentes
* **FASE 3(L3)**: El sistema final

Habiendo realizado previamente las dos primeras fases, en esta rama se construye el sistema final. Este sistema final se compone
de un cliente, tres orchestrators, una factoría de downloaders y una factoría de transfers.
Una vez creada la infraestructura del sistema, el cliente podrá mandar una URL a un orchestrator que a su vez lo reenviará
a un downloader, que descargará el archivo (si no ha sido descargado previamente) y lo pondra a disposición de los
orchestrator mediante un canal de eventos.

El cliente podrá solicitar la lista de ficheros descargados a un orchestrator y podrá también pedir la transferencia de un archivo
de audio a un orchestrator que reenviara esa petición a un transfer (si el archivo se ha descargado previamente) para que el
transfer lo envie directamente al cliente.

Destacar que, los orchestrator deben comunicarse entre ellos para anunciar su creación con el objetivo de actualizar las listas
de orchestrators existentes de cada objeto.

## DIAGRAMA DEL SISTEMA
<p align="center">
  <img width="653" height="776" src="https://i.gyazo.com/f079e813d0bf8f8909f31fd5fa9b68e8.png">
</p>

## MANUAL DEL USUARIO
**¿CÓMO EJECUTAR EL SISTEMA?**

**1)** Ejecutar el comando make y abrir la interfaz gráfica de Ice
```
~$ make run
~$ icegridgui
```
**2)** Crear una nueva conexion con el registro
```
Pulsar boton Log into an IceGrid Registry -> New Conection -> Direct Conection -> Seleccionar el registry -> Poner contraseña y crear la conexión -> Pulsar Next
```
**3)** Abrir el archivo xml
```
Open-> Application from File -> YoutubeDownloaderApp.xml
```
**4)** Cargar la aplicación en el registro y distribuir
```
1) Save to a registry
2) En Live Deployment Tools -> Application -> Path distribution
```
**5)** Ejecutar los nodos por orden
```
Icestorm > Downloads-node > Orchestrators-node
```
**6)** Ejecutar el comando
```
~$ ./run_client.sh
```

## DESCRIPCIÓN DE LOS COMPONENTES DEL SISTEMA
**Servidor**
#### downloader_factory.py:
Es el componente encargado de la descarga de ficheros, y son creados bajo demanda mediante una factoría de objetos. Una vez que recibe una peticion, procederá a descargarla, y cuando la descargue, avisará a los orchestrator de que se ha bajado el archivo, para, después, autodestruirse.
#### transfer_factory.py:
El transfer es el componente encargado de la transferencia de ficheros, y, al igual que el anterior, son creados bajo demanda
mediante una factoría de objetos para poder recibir peticiones de transferencia.
- Cuando reciba la petición, creará la tarea para que el transfer transfiera el audio de forma similar a como se realiza el envío de información por medio de sockets en python, y al finalizar ésta, es destruido. [close()-destroy()]
#### orchestrator.py:
Se encarga de la gestión de los downloaders, haciendo de intermediario entre éstos y el  cliente. Es una de las partes que actúan del 
servidor y pueden existir uno o varios. Además, estas siempre a la espera de recibir nuevas peticiones por parte del cliente.
- Cabe destacar, que éstas son asignadas a downloaders y transfers, después de haber solicitado su creación. 
- También mantiene listas actualizadas de los ficheros ya  descargados en el sistema controlando los eventos del canal de actualizaciones y proporcionará la lista de ficheros disponibles (ya descargados e indexados)de todos los downloaders del sistema.
- Finalmente, Cuando se arranca un nuevo orchestrator saluda al resto de orchestrators, que se anuncian al nuevo objeto.

**Cliente**
#### client.py:
El cliente  se conecta a cualquiera de los orchestrators para solicitar información o la descarga de ficheros. En esta fase solicitará descargas, transferencias o la lista de ficheros a cualquiera de los orchestrators: recibe una URL como argumento para descargar, el nombre de un fichero para una transferencia, y si no recibe nada, la lista los ficheros que haya en el sistema.

