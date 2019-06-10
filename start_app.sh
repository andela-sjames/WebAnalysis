#!/usr/bin/env bash

# host.docker.internal:0

xhost + 127.0.0.1
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
docker run -it --name=dwa -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix:rw webanalysis
