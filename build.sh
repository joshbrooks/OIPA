docker build --build-arg HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+') -t oipa -f oipa-server.Dockerfile .
