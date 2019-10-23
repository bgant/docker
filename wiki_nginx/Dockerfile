# Source: https://wiki.alpinelinux.org/wiki/MediaWiki
#
# 127.0MB  mybuild (alpine:latest + mediawiki + lighttpd + php7 + sqlite)
# 737.0MB  mediawiki:latest (debian + mediawiki + apache + php + sqlite)
#  87.4MB  php:rc-alpine
#  21.2MB  nginx:alpine
#   5.6MB  alpine:latest

FROM alpine:latest

# Patch Alpine Linux
#RUN apk update && apk upgrade  # Docker will cache this command and it will never run in the future unless full rebuild 

# Install web server
RUN apk update && apk add nginx openssl
RUN mkdir /run/nginx
RUN mv -v /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled

# Install openssl files (create with generate-openssl.sh)
COPY localhost.crt /etc/ssl/certs/localhost.crt
COPY localhost.key /etc/ssl/private/localhost.key

# Download latest MediaWiki version       
RUN apk update && apk add bash html-xml-utils           
COPY download-mediawiki.sh /opt/               
RUN /bin/bash /opt/download-mediawiki.sh

# Install PHP files

# Install database
#RUN apk update && apk add sqlite php7-sqlite3

# Install MediaWiki required packages
#RUN apk update && apk add imagemagick diffutils

# Make network ports available
EXPOSE 80 443

# From nginx Dockerfile
# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# From nginx Dockerfile
CMD ["nginx", "-g", "daemon off;"]

