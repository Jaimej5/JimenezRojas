#!/usr/bin/python3
# -*- coding: utf-8 -*-


import Ice

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
		cancion = input()
		msg = orchestrator.downloadTask(cancion)
        print('El gestor de descargas responde: ',msg,'\n\n')

    def run(self, argv):
		



        return 0

sys.exit(Client().main(sys.argv))