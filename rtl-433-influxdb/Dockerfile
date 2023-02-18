FROM ubuntu:jammy-20221101

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y rtl-433
COPY rtl-433-influxdb.sh /
ENTRYPOINT ["/rtl-433-influxdb.sh"]
