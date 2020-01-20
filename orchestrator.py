#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413


class OrchestratorI(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''

    orchestrator = None

    def downloadTask(self, url, current=None):
        '''
        downloadTask
        '''
        if self.orchestrator:
            return self.orchestrator.send_downloadTask(url)

    def getFileList(self, current=None):
        '''
        getFileList
        '''
        if self.orchestrator:
            return self.orchestrator.get_file_list()
        return []

    def getFile(self, name, current=None):
        '''
        getFile
        '''
        if self.orchestrator:
            return self.orchestrator.get_file(name)
        return None

    def announce(self, other, current=None):
        '''
        announce
        '''
        if self.orchestrator:
            self.orchestrator.new_orchestrator(other)

class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    '''
    OrchestratorEventI
    '''
    orchestrator = None

    def hello(self, me, current=None):
        '''
        Hello
        '''
        if self.orchestrator:
            self.orchestrator.say_hello_to(me)

class FileUpdatesEventI(TrawlNet.UpdateEvent):
    '''
    FileUpdateEventI
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        '''
        newFile
        '''
        if self.orchestrator:
            file_hash = file_info.hash
            if file_hash not in self.orchestrator.files:
                print(file_info.name)
                print(file_info.hash)
                self.orchestrator.files[file_hash] = file_info.name

class Orchestrator():
    '''
    OrchestratorClass
    '''

    def __init__(self, broker, sync_topic, files_updates_topic):
        '''
        Init
        '''
        self.files = {}
        self.orchestrators = {}
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        downloader_factory = TrawlNet.DownloaderFactoryPrx.checkedCast(broker.propertyToProxy("DownloaderFactoryIdentity"))
        self.downloader = downloader_factory.create()

        self.transfer_factory = TrawlNet.TransferFactoryPrx.checkedCast(broker.propertyToProxy("TransferFactoryIdentity"))

        self.sync_topic = sync_topic
        self.servant = OrchestratorI()
        self.servant.orchestrator = self
        propiedad = broker.getProperties().getProperty("Identity")
        self.proxy = self.adapter.add(self.servant, broker.stringToIdentity(propiedad))
        #self.proxy = self.adapter.addWithUUID(self.servant)

        #Create Orchestrator servant
        self.subscriber = OrchestratorEventI()
        self.subscriber.orchestrator = self
        self.subscriber_proxy = self.adapter.addWithUUID(self.subscriber)
        self.sync_topic.subscribeAndGetPublisher({}, self.subscriber_proxy)

        #Create Orchestrator Event publisher
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.sync_topic.getPublisher())
        # Create fileUpdates Event subscriber


        self.fileUpdates = FileUpdatesEventI()
        self.fileUpdates.orchestrator = self
        self.fileUpdatesTopic = files_updates_topic # Obtener el topic de fileUpdatesTopic
        self.fileUpdatesProxy = self.adapter.addWithUUID(self.fileUpdates)
        self.fileUpdatesTopic.subscribeAndGetPublisher({}, self.fileUpdatesProxy)

    def send_downloadTask(self, url):
        '''
        send_downloadTask
        '''
        return self.downloader.addDownloadTask(url)

    def say_hello_to(self, orchestrator):
        '''
        say_hello_to
        '''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("New orchestrator: %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy))


    def new_orchestrator(self, orchestrator):
        '''
        new_orchestrator
        '''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print(" previous orchestartor %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator

    def get_file_list(self):
        '''
        get_file_list
        '''
        fileList = []
        for fileHash in self.files:
            fileInfo = TrawlNet.FileInfo()
            fileInfo.hash = fileHash
            fileInfo.name = self.files[fileHash]
            fileList.append(fileInfo)
        return fileList

    def get_file(self, name):
        '''
        get_file
        '''
        try:
            return self.transfer_factory.create(name)
        except:
            raise TrawlNet.TransferError("Error en la transferencia del fichero")

    def start(self):
        '''
        start
        '''
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy))


class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Server
    '''
    sync_topic = None
    files_topic = None
    UPDATE_EVENTS = "UpdateEvents"
    ORCHESTRATOR_SYNC = "OrchestratorSync"

    def run(self, argv):
        '''
        Iniciar servidor
        '''
        broker = self.communicator()
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            return 2

        self.sync_topic = self.create_topic(self.ORCHESTRATOR_SYNC, topic_mgr)
        self.files_topic = self.create_topic(self.UPDATE_EVENTS, topic_mgr)

        orchestrator = Orchestrator(broker, self.sync_topic, self.files_topic)
        orchestrator.start()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

    def create_topic(self, topic_name, topic_mgr):
        try:
            return topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            return topic_mgr.create(topic_name)


    def get_topic_manager(self):
        key = 'YoutubeDownloaderApp.IceStorm/TopicManager'
        proxy = self.communicator().stringToProxy(key)
        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

ORCHESTRATOR = Server()
sys.exit(ORCHESTRATOR.main(sys.argv))
