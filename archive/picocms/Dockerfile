# Source: http://picocms.org/docs/#i-want-to-use-composer
FROM php:8.0.25-apache-buster

#ARG DEBIAN_FRONTEND=noninteractive
#ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y git unzip
RUN curl -sSL https://getcomposer.org/installer | php
RUN php /var/www/html/composer.phar create-project --no-install picocms/pico-composer pico
WORKDIR /var/www/html/pico
RUN php /var/www/html/composer.phar config --no-plugins allow-plugins.picocms/composer-installer true  
RUN php /var/www/html/composer.phar install
RUN a2enmod rewrite

