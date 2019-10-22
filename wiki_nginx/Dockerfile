# Source: https://wiki.alpinelinux.org/wiki/MediaWiki
#
# 127.0MB  mybuild (alpine:latest + mediawiki + lighttpd + php7 + sqlite)
# 737.0MB  mediawiki:latest (debian + mediawiki + apache + php + sqlite)
#  87.4MB  php:rc-alpine
#  21.2MB  nginx:alpine
#   5.6MB  alpine:latest

FROM alpine:latest

# Patch Alpine Linux
RUN apk update && apk upgrade

# Install web server
RUN apk add nginx openssl
RUN mkdir /run/nginx
COPY openssl_self_signed_cert.conf /opt
RUN cd /opt && openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -config openssl_self_signed_cert.conf
RUN cp localhost.crt /etc/ssl/certs/localhost.crt && cp localhost.key /etc/ssl/private/localhost.key

# Download latest MediaWiki version       
RUN apk add bash html-xml-utils           
COPY download-mediawiki.sh /opt/               
RUN /bin/bash /opt/download-mediawiki.sh

# Install database
#RUN apk add sqlite php7-sqlite3

# Install MediaWiki required packages
#RUN apk add imagemagick diffutils

# Make network ports available
EXPOSE 80 443
