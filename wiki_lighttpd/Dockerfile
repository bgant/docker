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
RUN apk add lighttpd
RUN sed -i 's/htdocs/htdocs\/mediawiki/' /etc/lighttpd/lighttpd.conf
RUN sed -i 's/#   include "mod_fastcgi.conf"/include "mod_fastcgi.conf"/' /etc/lighttpd/lighttpd.conf
RUN mkdir /var/run/lighttpd && chown lighttpd:root /var/run/lighttpd

# Download latest MediaWiki version       
RUN apk add bash html-xml-utils           
COPY download-mediawiki.sh /opt/               
RUN /bin/bash /opt/download-mediawiki.sh

# Install PHP
#RUN apk add php7 php7-dom php7-json php7-iconv php7-zlib php7-gd php7-cgi
RUN apk add php7 php7-cgi php7-mbstring php7-ctype php7-xml php7-fileinfo php7-json php7-iconv

# Install database
RUN apk add sqlite php7-sqlite3

# Install MediaWiki required packages
#RUN apk add imagemagick diffutils

# Make network ports available
EXPOSE 80 443
