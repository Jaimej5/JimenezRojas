#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

#Imports
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet
import download_mp3 as dwmp3
import sys


class Downloader(TrawlNet.Downloader):
	#Metodo para descargar la URL
    def anadirdescarga(self, url):
        print("URL recibida: ",url)
        print("Descargando URL: ",url)
		print("URL descargada: ")
        return dwmp3.download_mp3(url)

#Servidor
class Server(Ice.Application):
	
	def run(self,argv):
	
		downloader = Downloader()
		comunicador = self.communicator()
		adaptador = comunicador.createObjectAdapter("Downloader_Adapter")
		DownloaderAdapter = adapter.add(downloader,comunicador.stringToIdentity("downloader"))
	
		print("'{}'".format(DownloaderAdapter),flush=True)
		adaptador.activate()
		self.shutdownOnInterrupt()
		comunicador.waitForShutdown()
	
		return 0

server = Server()
sys.exit(server.main(sys.argv))
