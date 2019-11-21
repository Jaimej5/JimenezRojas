#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-


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


_YOUTUBEDL_OPTS_  = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}

def download_mp3(url,destination='./'):

	options = {}
	task_status = {}
	
	def progress_hook(status):
		task_status.update(status)
	
	options.update(_YOUTUBEDL_OPTS_)
	options['progress_hooks'] = [progress_hook]
	options['outtmpl'] = os.path.join(destination,'%(title)s.%(ext)s')
	
	with youtube_dl.YoutubeDL(options) as youtube:
		youtube.download([url])
	
	filename = task_status['filename']
	filename = filename[:filename.rindex('.') + 1]
	return filename + options['postprocessors'][0]['preferredcodec']
	
		
	
	