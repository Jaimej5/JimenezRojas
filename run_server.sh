#!/bin/sh



./downloader.py --Ice.Config=downloader.config | tee proxy.out &

arg_prx=$(tail -1 proxy.out)

./orchestrator.py --Ice.Config=orchestrator.config "$arg_prx"



