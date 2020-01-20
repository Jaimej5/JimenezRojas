#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader.py
'''

import sys
import hashlib
import os.path
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

from download_mp3 import download_mp3
from download_mp3 import hash_fichero

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
    publisher = None

    def __init__(self, publisher):
        self.publisher = publisher

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        addDownloadTask
        '''
        descarga = download_mp3(url)
        if not descarga:
            raise TrawlNet.DownloadError("Error")

        file_info = TrawlNet.FileInfo()
        file_info.name = os.path.basename(descarga)
        file_info.hash = hash_fichero(file_info.name)

        if self.publisher:
            self.publisher.newFile(file_info)
            
        return file_info

    def destroy(self, current):
        ''' Destroy '''
        try:
            current.adapter.remove(current.id)
        except Exception as e:
            print(e, flush=True)

        
class DownloaderFactoryI(TrawlNet.DownloaderFactory):
    publisher = None

    def __init__(self, publisher):
        self.publisher = publisher

    def create(self, current):
        ''' Create '''
        servant = DownloaderI(self.publisher)
        proxy = current.adapter.addWithUUID(servant)
        return TrawlNet.DownloaderPrx.checkedCast(proxy)


class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''
    def run(self, argv): # pylint: disable=W0613,W0221
        '''
        Run
        '''
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        key = 'YoutubeDownloaderApp.IceStorm/TopicManager'
        topic_name = "UpdateEvents"
        proxy = self.communicator().stringToProxy(key)
        
        if proxy is None:
            return None

        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101
        if not topic_mgr:
            return 2

        try:
            topic_file = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic_file = topic_mgr.create(topic_name)

        publisher = TrawlNet.UpdateEventPrx.uncheckedCast(topic_file.getPublisher())
        properties = broker.getProperties()

        downloader = DownloaderFactoryI(publisher)
        factory_id = properties.getProperty('DownloaderFactoryIdentity')
        proxy = adapter.add(downloader, broker.stringToIdentity(factory_id))

        print(proxy, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

SERVER = Server()
sys.exit(SERVER.main(sys.argv))
