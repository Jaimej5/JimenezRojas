#!/usr/bin/python3
# -*- coding: utf-8 -*-


import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet
import sys

class Client(Ice.Application):
    def __init__(self):
        print('Cliente iniciado\n\n')

    def principal(self, current=None):
        print('-----------------------------------------------------------------')
        print('|                  Descargar música de YouTube  				   |')
        print('-----------------------------------------------------------------')
        print('\nElige una opción:')
        print('1. Descargar canción')
        print('2. Salir')

    def descargarSong(self, orchestrator, current=None):
		print('Introduce la URL de la canción que quieres descargar')
		name = input()
		message = orchestrator.downloadTask(name)
        print('El gestor de descargas responde: ',message,'\n\n')

    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Invalid orchestrator proxy')

        orchestrator.downloadTask(argv[2])
        
		return 0

sys.exit(Client().main(sys.argv))