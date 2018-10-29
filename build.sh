#!/bin/bash
HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
container=oipa

docker build --build-arg HOST=${HOST} -t ${container} -f oipa-server.Dockerfile .
