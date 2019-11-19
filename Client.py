#!/usr/bin/python3
# -*- coding: utf-8 -*-


import Ice

import sys

class Client(Ice.Application):
    def __init__(self):
        print('Cliente iniciado\n\n')

    def principal(self, current=None):
        print('/////////////////////////////////////////////////////////////////')
        print('// Bienvenido a la aplicacion para descargar musica de Youtube //')
        print('/////////////////////////////////////////////////////////////////')
        print('\nSelecciona la opcion que desees')
        print('1. Descargar cancion')
        print('2. Salir')

    def descargarSong(self, orchestrator, current=None):
        print('El gestor de descargas responde: ',message,'\n\n')

    def run(self, argv):




        return 0

sys.exit(Client().main(sys.argv))