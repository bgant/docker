FROM python:3.12.7-alpine3.20
ENV TZ="US/Central"
WORKDIR /usr/src/app
RUN apk update && apk add --no-cache rtl_433 
RUN pip install --no-cache-dir requests
COPY pipe-json.py ./
COPY webdis.py ./
COPY rtl-433.sh ./

#COPY . .
#CMD [ "python", "./your-daemon-or-script.py" ]

# docker build -t python-rtl-433 .
# docker run -it --rm -v /home/docker/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto:/usr/src/myapp -w /usr/src/myapp python-pip python light_control.py
