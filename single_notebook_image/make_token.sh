#!/bin/bash
#openssl rand -hex 32 > token.txt
export JUPYTER_TOKEN=`cat token.txt`
echo ${JUPYTER_TOKEN}
# xdg-open http://127.0.0.1:8445?token=${JUPYTER_TOKEN}

