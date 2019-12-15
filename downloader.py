#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader
'''

import sys
import os.path
import Ice # pylint: disable=E0401
import IceStorm  # pylint: disable=W0611
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413
from topic_icestorm import Topics
import download_mp3 as download


class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''
    def run(self, argv): # pylint: disable=W0613,W0221
        ''' Run '''
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        downloader = DownloaderI()
        topics = Topics(broker)
        topic_archivos = topics.topic_archivos
        downloader.publisher = TrawlNet.UpdateEventPrx.uncheckedCast(topic_archivos.getPublisher())
        proxy = adapter.addWithUUID(downloader)
        print(proxy, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    DownloaderI
    '''
    publisher = None

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        ''' addDownloadTask '''
        try:
            archivo_descarga = download.download_mp3(url)
        except:
            raise TrawlNet.DownloadError("Error")

        archivo_info = TrawlNet.FileInfo()
        archivo_info.name = os.path.basename(archivo_descarga)
        archivo_info.hash = download.hash_fichero(archivo_info.name)

        if self.publisher:
            self.publisher.newFile(archivo_info)
        return archivo_info



SERVER = Server()
sys.exit(SERVER.main(sys.argv))
