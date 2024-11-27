FROM python:3.12.7-alpine3.20
ENV TZ="US/Central"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .
#CMD [ "python", "./your-daemon-or-script.py" ]

# docker build -t python-pip .
# docker run -it --rm -v /home/docker/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto:/usr/src/myapp -w /usr/src/myapp python-pip python light_control.py
