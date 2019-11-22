#!/bin/sh

./downloader.py --Ice.Config=downloader.config | tee proxy_down.out &

sleep 3

./orchestrator.py --Ice.Config=orchestrator.config "$(head -1 proxy_down.out)"


