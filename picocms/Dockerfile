# Source: http://picocms.org/docs/#i-want-to-use-composer
FROM php:8.0.1-apache-buster

#ARG DEBIAN_FRONTEND=noninteractive
#ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y git unzip
RUN curl -sSL https://getcomposer.org/installer | php
RUN php composer.phar create-project picocms/pico-composer pico
RUN a2enmod rewrite

