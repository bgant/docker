FROM docker.io/library/python:3.12.7-alpine3.20
ENV TZ="US/Central"
WORKDIR /usr/src/app
RUN apk update && apk add --no-cache rtl_433 
RUN pip install --no-cache-dir requests
COPY *.py ./
COPY *.sh ./
CMD [ "./main.sh" ]

# docker build -t python-rtl-433 .
# docker run -it --rm --device=/dev/bus/usb:/dev/bus/usb python-rtl-433
# docker run -it --rm --device=/dev/bus/usb:/dev/bus/usb python-rtl-433 /bin/sh  <-- run commands manually in container

# Difference between RUN, CMD, ENTRYPOINT:
# https://www.baeldung.com/ops/dockerfile-run-cmd-entrypoint
