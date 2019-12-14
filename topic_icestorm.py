 #!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

''' Creating topics Icestorm class '''

import IceStorm

class Topics:
    '''
    Class Topics
    '''

    update_sync = "UpdateEvents"
    orchestrator_sync = "OrchestratorSync"

    def __init__(self, broker):
        ''' Constructor '''
        self.topic_mgr = self.get_topic_manager(broker)
        self.topic_archivos = self.get_topic(self.topic_mgr, self.update_sync)
        self.topic_orchestrator = self.get_topic(self.topic_mgr, self.orchestrator_sync)
        
    def get_topic_manager(self, broker):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = broker.propertyToProxy(key)
        if proxy is None:
            print("Proxy no valido")
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def get_topic(self, topic_mgr, topic_name):
        ''' Get topic or create '''
        try:
            return topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            return topic_mgr.create(topic_name)
    