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
1) downloader_factory.py
2) transfer_factory.py
3) orchestrator.py

**Cliente**
1) client.py

