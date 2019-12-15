#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-


import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

from topic_icestorm import Topics

class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''
    def run(self, argv):
        '''
        Iniciar
        '''
        broker = self.communicator()
        topics = Topics(broker)
        topic_archivos = topics.topic_archivos
        topic_orchestrator = topics.topic_orchestrator
        Orchestrators(broker, argv[1], topic_archivos, topic_orchestrator)
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0


class Orchestrators:
    '''
    Orchestrator Managing class 
    '''
    files = {}
    orchestrators = {}
    qos = {}

    def __init__(self, broker, downloader_proxy, topic_archivos, topic_orch):
        ''' Builder '''
        self.run(broker, downloader_proxy, topic_archivos, topic_orch)
        self.start_orchestrator()

    def downloadTask(self, url):
        ''' downloadTask '''
        return self.downloader.addDownloadTask(url)


    def new(self, orchestrator):
        ''' New orchestrator in the system ''' 
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hey! I am orchestrartor %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator

    def hi(self, orchestrator):
        ''' Hi '''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hi! orchestrator %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy))

    def start_orchestrator(self):
        ''' Starting orchestrator '''
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy))

    def get_songs(self):
        ''' Get Songs List '''
        filelist = []
        for fileHash in self.files:
            fileInfo = TrawlNet.FileInfo()
            fileInfo.hash = fileHash
            fileInfo.name = self.files[fileHash]
            filelist.append(fileInfo)
        return filelist

    def run(self, broker, downloader_proxy, topic_archivos, topic_orch):
        ''' Running all elements '''
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_proxy))
       
        self.orchestrator_topic = topic_orch
        self.orchestrator_servant = OrchestratorI()
        self.orchestrator_servant.orchestrator = self
        self.proxy = self.adapter.addWithUUID(self.orchestrator_servant)

        self.subscriber = OrchestratorEventI()
        self.subscriber.orchestrator = self
        self.subscriber_proxy = self.adapter.addWithUUID(self.subscriber)
        self.orchestrator_topic.subscribeAndGetPublisher(self.qos, self.subscriber_proxy)
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.orchestrator_topic.getPublisher())

        self.file_updates_event = FileUpdatesEventI()
        self.file_updates_event.orchestrator = self
        self.file_topic = topic_archivos
        self.file_updates_event_proxy = self.adapter.addWithUUID(self.file_updates_event)
        self.file_topic.subscribeAndGetPublisher(self.qos, self.file_updates_event_proxy)

    def __str__(self):
        ''' str '''
        return str(self.subscriber_proxy) 

class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    '''
    OrchestratorEventI
    '''
    orchestrator = None

    def hello(self, orchest, current=None):
        '''
        Hola!
        '''
        if self.orchestrator:
            self.orchestrator.hi(orchest)

class FileUpdatesEventI(TrawlNet.UpdateEvent):
    '''
    FileUpdatesEventI
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        ''' newFile '''
        if self.orchestrator:
            file_hash = file_info.hash
            if file_hash not in self.orchestrator.files:
                print("New File name", file_info.name)
                print("New File hash", file_info.hash)
                self.orchestrator.files[file_hash] = file_info.name

class OrchestratorI(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''
    orchestrator = None

    def getFileList(self, current=None):
        ''' getFileList '''
        if self.orchestrator:
            return self.orchestrator.get_songs()
        else:
            return []

    def downloadTask(self, url, current=None):
        ''' downloadTask '''
        if self.orchestrator:
            return self.orchestrator.downloadTask(url)

    def announce(self, another, current=None):
        ''' Announce orchestrator '''
        if self.orchestrator:
            self.orchestrator.new(another)


SERVER = Server()
sys.exit(SERVER.main(sys.argv))
