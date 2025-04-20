FROM python:3.13.3-alpine3.21
ENV TZ="US/Central"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .
#CMD [ "python", "./your-daemon-or-script.py" ]

# podman build -f Dockerfile -t python-pip:latest
# podman run -it --rm -v /home/docker/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto:/usr/src/myapp -w /usr/src/myapp python-pip python light_control.py
# <No -it (interactive and terminal TTY) in crontab scripts!>
