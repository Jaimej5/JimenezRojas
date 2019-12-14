#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Orchestrator
'''

import sys
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

songs = []

class UpdateEventI(TrawlNet.UpdateEvent):
    files = {}

    def newFile(self, fileInfo, current=None):
        fileHash = fileInfo.hash
        if fileHash not in self.files:
            print(fileInfo.name)
            print(fileInfo.hash)
            self.files[fileHash] = fileInfo.name


class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    def hello(self, orchestrator, current=None):
        orchestrator.announce(orchestrator)


class OrchestratorI(TrawlNet.Orchestrator): #pylint: disable=R0903
    '''
    Orchestrator Module
    '''
    files = {}

    def __init__(self, files):
        self.files = files

    def announce(self, orchestrator, current=None):
        print("Recibido ",orchestrator)

    def setTopicandDownloader(self, downloader, topic_orch):
        orchestrators = topic_orch.getPublisher()
        self.downloader = downloader
        subscritos = TrawlNet.OrchestratorEventPrx.uncheckedCast(orchestrators)
        subscritos.hello(TrawlNet.OrchestratorPrx.checkedCast(self.prx))

    def setProxy(self, prx):
        self.prx = prx

    def downloadTask(self, url, current=None): # pylint: disable=C0103, W0613
        '''
        Function download task
        '''
        print(url)
        return self.downloader.addDownloadTask(url)

    def getFileList(self, current=None):
        songs = []
        for fileHash in self.files:
            fileInfo = TrawlNet.FileInfo()
            fileInfo.hash = fileHash
            fileInfo.name = self.files[fileHash]
            songs.append(fileInfo)
        return songs


class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''
    files = {}
    def run(self, argv):
        '''
        Iniciar servidor
        '''
        key = "IceStorm.TopicManager.Proxy"
        topic_name = "UpdateEvents"
        topic_orchestrator = "OrchestratorSync"
        qos_orch = {}
        qos = {}
        proxy = self.communicator().propertyToProxy(key)
        print("Using IceStorm in '%s'" % key)

        if proxy is None:
            return None
        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy)
        if not topic_mgr:
            print("Invalid proxy")
            return 2

        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        downloader_instance = TrawlNet.DownloaderPrx.checkedCast(proxy)
        if not downloader_instance:
            raise RuntimeError('Invalid proxy')

        updateEvent = UpdateEventI()
        files = updateEvent.files
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        evt_ficheros = adapter.addWithUUID(updateEvent)

        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, evt_ficheros)

        evtorchestrators = OrchestratorEventI()
        evt_orchestrators = adapter.addWithUUID(evtorchestrators)

        try:
            topicorch = topic_mgr.retrieve(topic_orchestrator)
        except IceStorm.NoSuchTopic:
            topicorch = topic_mgr.create(topic_orchestrator)

        topicorch.subscribeAndGetPublisher(qos_orch, evt_orchestrators)

        orchestrator = OrchestratorI(files)
        proxy_orchestrator = adapter.add(orchestrator, broker.stringToIdentity("orchest"))

        orchestrator.setProxy(proxy_orchestrator)
        orchestrator.setTopicandDownloader(downloader_instance, topicorch)
        print(proxy_orchestrator)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


ORCHEST = Server()
sys.exit(ORCHEST.main(sys.argv))
