# Source: https://wiki.alpinelinux.org/wiki/MediaWiki
#
# 127.0MB  mybuild (alpine:latest + mediawiki + lighttpd + php7 + sqlite)
# 737.0MB  mediawiki:latest (debian + mediawiki + apache + php + sqlite)
#  87.4MB  php:rc-alpine
#  21.2MB  nginx:alpine
#   5.6MB  alpine:latest

FROM alpine:latest

# "You don't upgrade in builds"
# "Running containers should not be modified (containers should be immutable and stateless)"
# "Put your containers behind a load balancer and it can be a zero-downtime thing"
# "Updates are baked into the base images so you should not apt-get upgrade your containers"
# "This updates all packages — which is bad because it prevents Dockerfile from creating consistent, immutable builds."
#RUN apk update && apk upgrade  # This runs once during build, is cached, and will never run again
# Source: https://runnable.com/blog/9-common-dockerfile-mistakes

# Install web server
RUN apk update && apk add nginx openssl
RUN mkdir /run/nginx
RUN mv -v /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled

# Install openssl files (create with generate-openssl.sh)
COPY localhost.crt /etc/ssl/certs/localhost.crt
COPY localhost.key /etc/ssl/private/localhost.key

# Install database
#RUN apk update && apk add sqlite php7-sqlite3

# Install MediaWiki required packages
#RUN apk update && apk add imagemagick diffutils

# Make network ports available
EXPOSE 80 443

# From nginx Dockerfile
# Source: https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile
# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log
CMD ["nginx", "-g", "daemon off;"]
