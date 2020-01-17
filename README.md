## Practica Sistemas distribuidos
https://github.com/Jaimej5/JimenezRojas

## Enunciado 
Por hacer

## Diagrama 
<p align="center">
  <img width="400" height="300" src="">
</p>

## Integrantes
Jaime Jimenez Catalán y Alvaro Rojas Parra

## Ramas
--------
* Entrega 1 -> L1
* Entrega 2 -> L2
* Entrega 3 -> L3

## Manual de usuario
**¿Cómo ejecutar?**

1) Ejecutar el comando make y abrir la interfaz gráfica de Ice
```
~$ make run
~$ icegridgui
```
2) Crear una nueva conexion con el registro
```
Pulsar boton Log into an IceGrid Registry -> New Conection -> Direct Conection -> Seleccionar el registry -> Poner contraseña y crear la conexión -> Pulsar Next
```
3) Abrir el archivo xml
```
Open-> Application from File -> YoutubeDownloaderApp.xml
```
4) Cargar la aplicación en el registro y distribuir
```
1) Save to a registry
2) En Live Deployment Tools -> Application -> Path distribution
```
5) Ejecutar los nodos por orden
```
Icestorm > Downloads-node > Orchestrators-node
```
6) Ejecutar el comando
```
./run_client.sh
```

### Descripción de los componentes del sistema
Por hacer
**Servidor**
1) downloader_factory.py
2) transfer_factory.py
3) orchestrator.py

**Cliente**
1) client.py

