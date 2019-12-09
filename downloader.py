#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader: Servidor
'''

import sys
import hashlib
import os.path
import youtube_dl #pylint: disable=E0401
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    DownloaderImplementation
    '''
    publisher = None

    def __init__(self, event):
        self.event_file = event

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Add Download Task
        '''
        file = download_mp3(url)
        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(file)
        fileInfo.hash = compute_hash(fileInfo.name)
        orchestrators = self.event_file.getPublisher()
        ##Downloader exception
        event = TrawlNet.UpdateEventPrx.uncheckedCast(orchestrators)
        event.newFile(fileInfo)
        return fileInfo