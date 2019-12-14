#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Cliente
'''
import sys
import Ice # pylint: disable=E0401,E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class Client(Ice.Application): # pylint: disable=R0903
    '''
    Clase cliente
    '''
    def __init__(self):
        print('Cliente iniciado\n\n')

    def run(self, argv):
        '''
        Iniciar cliente
        '''
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Invalid orchestrator proxy')

        if(len(argv)==2):
            print('Lista de canciones preparadas para: ' , orchestrator)
            file_list = orchestrator.getFileList()
            print(file_list)
        elif(len(argv)==3):
            orchestrator.downloadTask(argv[2])
        else:
            ("Introduzca los argumentos correctamente")

        return 0

sys.exit(Client().main(sys.argv))
