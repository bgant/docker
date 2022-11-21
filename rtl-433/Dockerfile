FROM ubuntu:jammy-20221101

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y rtl-433

# -R 76 specifies device decoding protocol for only the LaCrosse TX29 at 915MHZ
CMD ["rtl_433","-f","915M","-R","76","-s","250k","-F","syslog::1433","-vv"]

