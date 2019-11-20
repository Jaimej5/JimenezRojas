#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-



import Ice
import sys

class Orchestrator(TrawlNet.Orchestrator):
    def __init__(self, param):
        self.downloader = param

    def downloadTask(self, url, current=None):
        reply = 'respuesta de Orchestrator'

        print('url',url,' enviada a ',self.downloader)
        reply_downloader=self.downloader.anadirdescarga(url)
        return reply+reply_downloader