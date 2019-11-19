#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import Ice

import sys
class Downloader():

    def addDownloadTask(self, url):
        print("URL recibida ",url)
        print("descargando")
        return "Descarga" +url+"finalizada"
		
class Server(Ice.Application):
	def run(self,argv):