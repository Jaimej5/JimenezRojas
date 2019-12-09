!/usr/bin/env python3
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