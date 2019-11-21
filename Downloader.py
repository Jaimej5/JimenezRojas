#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-


import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet
import download_mp3 as dw
import sys


class Downloader(TrawlNet.Downloader):

    def addDownloadTask(self, url, current=None):
        print("URL recibida: ",url)
        print("Descargando URL: ",url)
		print("URL descargada: ")
        return dw.download_mp3(url)


class Server(Ice.Application):
	
	def run(self,argv):
	
		downloader = Downloader()
		broker = self.communicator()
		adapter = broker.createObjectAdapter("DownloaderAdapter")
		prx_downloader = adapter.add(downloader,broker.stringToIdentity("downloader"))
	
		print("'{}'".format(prx_downloader),flush=True)
		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
	
		return 0

server = Server()
sys.exit(server.main(sys.argv))
