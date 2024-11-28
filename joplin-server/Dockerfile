FROM joplin/server:3.0.1-beta

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
USER root
RUN apt-get update && apt-get install -y curl --no-upgrade
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
USER joplin

# docker build -t joplin-server-curl .
