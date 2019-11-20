#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

#Imports
import os.path
try:
	import youtube_dl
except ImportError:
	print('Error al importar youtube_dl')
	sys.exit(1)

class NullLogger:
	def debug(self,msg): pass
	def warning(self,msg): pass
	def error(self,msg): pass

#Opciones de descarga de YouTube
_YOUTUBEDL_OPTS_  = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}

def download_mp3(URL,destino='./'):

	opciones = {}
	estado = {}
	
	def progreso(estado):
		estado.update(estado)
	
	opciones.update(_YTDL_OPTS)
	opciones['progreso'] = [progreso]
	opciones['salida'] = os.path.join(destino,'%(title)s.%(ext)s')
	
	with youtube_dl.YoutubeDL(options) as youtube:
		youtube.download([URL])
	
	archivo = estado['archivo']
	archivo = archivo[:archivo.rindex('.') + 1]
	return archivo + opciones['postprocessors'][0]['preferredcodec']
	
		
	
	