#!/bin/sh


#Ejecutar IceBox
rm -r IceStorm/

mkdir -p IceStorm/

sleep 2

sudo icebox --Ice.Config=icebox.config &

sleep 2

./downloader.py --Ice.Config=server.config | tee proxy_down.out &

sleep 2

./orchestrator.py --Ice.Config=server.config "$(head -1 proxy_down.out)"
