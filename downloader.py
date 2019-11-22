#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

'''
Downloader
'''

import sys
import os.path
import youtube_dl
import Ice  # pylint: disable=E0401, C0413
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401, C0413

class NullLogger:
    '''
    NullLogger
    '''
    def debug(self, msg):
        '''
        Debug
        '''
        pass

    def warning(self, msg):
        '''
        Warning
        '''
        pass

    def error(self, msg):
        '''
        Error
        '''
        pass


_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}


def download_mp3(url, destination='./music/'):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}

    def progress_hook(status):
        '''
        progress hook
        '''
        task_status.update(status)
    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')

    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']


class Downloader(TrawlNet.Downloader):
    '''
    Downloader
    '''
    def addDownloadTask(self, url, current=None):
        '''
        add task
        '''
        print("URL recibida", url)
        return download_mp3(url)

class Server(Ice.Application):
    '''
    server
    '''
    def run(self, argv):
        '''
        run
        '''
        downloader = Downloader()
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        prx_downloader = adapter.add(downloader, broker.stringToIdentity("downloader"))
        print(prx_downloader, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

SERVIDOR = Server()
sys.exit(SERVIDOR.main(sys.argv))
