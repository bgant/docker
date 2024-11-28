#!/bin/sh
docker run --rm -v /home/docker/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto:/usr/src/myapp -w /usr/src/myapp python-pip python light_control.py

# No docker run -it (interactive and terminal TTY) in crontab scripts!
