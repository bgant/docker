# docker-compose build for this image is run on k3s-113
FROM debian:buster-20210408-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y wget

RUN mkdir /fah
WORKDIR /fah

ENV FAH_VERSION=7.6.21
RUN wget https://download.foldingathome.org/releases/public/release/fahclient/debian-stable-arm64/v7.6/fahclient_${FAH_VERSION}_arm64.deb
RUN dpkg --unpack fah*.deb

CMD ["nice","/usr/bin/FAHClient","--chdir","/fah/"]
