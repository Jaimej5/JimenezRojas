#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet

import sys

class Orchestrator(TrawlNet.Orchestrator):
    def __init__(self, param):
        self.downloader = param

    def downloadTask(self, url, current=None):
        reply = 'respuesta de Orchestrator'

        print('url',url,' enviada a ',self.downloader)
        reply_downloader=self.downloader.addDownloadTask(url)
        return reply+reply_downloader

class Server(Ice.Application):
    def run(self, argv):

        prx_down = self.communicator().stringToProxy(argv[1])
        down = TrawlNet.DownloaderPrx.checkedCast(prx_down)
        if not down:
            raise RuntimeError('Proxy no valido')

        servidor = Orchestrator(param=down)
        adapter = self.communicator().createObjectAdapter("OrchestratorAdapter")
        prx_orch = adapter.add(servidor, self.communicator().stringToIdentity("orchestrator"))
        print("Orch esperando '{}'".format(prx_orch))
        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
