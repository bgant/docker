# Building my own separate php-fpm container with packages
# rather than using the compiled php:7-fpm-alpine image
#
# Source: https://github.com/docker-library/php/blob/master/7.3/alpine3.10/fpm/Dockerfile

FROM alpine:3

# Packages needed to reach MediaWiki additional PHP packages needed page
RUN apk update && apk add php7-fpm php7-mbstring php7-xml php7-xmlrpc php7-soap php7-ctype php7-json php7-iconv php7-fileinfo

# Packages needed to launch Mediawiki LocalSettings.php configuration pages
RUN apk update && apk add php7-session php7-dom

# Database software
# Source: https://www.mediawiki.org/wiki/Manual:Installing_MediaWiki#SQLite
RUN apk update && apk add php7-pdo_sqlite
RUN mkdir -vp /var/www/localhost/data && chown nobody:nobody /var/www/localhost/data

# Additional packages recommended by MediaWiki configuration page
RUN apk update && apk add php7-gd php7-intl php7-pecl-apcu php7-zip imagemagick diffutils

# Same settings as www.conf but with listen=0.0.0.0:9000 instead of 127.0.0.1:9000
RUN mv /etc/php7/php-fpm.d/www.conf /etc/php7/php-fpm.d/www.conf.disabled
COPY docker.conf /etc/php7/php-fpm.d/

RUN ln -sf /dev/stderr /var/log/php7/error.log

WORKDIR /var/www/html
EXPOSE 9000
STOPSIGNAL SIGQUIT
CMD ["php-fpm7"]
