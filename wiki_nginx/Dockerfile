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

# Install openssl files (create with generate-openssl.sh)
COPY localhost.crt /etc/ssl/certs/localhost.crt 
COPY localhost.key /etc/ssl/private/localhost.key

# Download latest MediaWiki version       
RUN apk add bash html-xml-utils           
COPY download-mediawiki.sh /opt/               
RUN /bin/bash /opt/download-mediawiki.sh

# Install PHP files

# Install database
#RUN apk add sqlite php7-sqlite3

# Install MediaWiki required packages
#RUN apk add imagemagick diffutils

# Make network ports available
EXPOSE 80 443
