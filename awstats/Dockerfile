# Apache2 Official httpd Container
FROM httpd:2.4.46

#ARG DEBIAN_FRONTEND=noninteractive
#ENV TZ=America/Chicago
RUN apt-get update && apt-get install -y libgeo-ip-perl libgeo-ipfree-perl wget


##################################################
# Setup Apache2
##################################################

# Add awstats settings to Apache2 configuration
RUN echo "Include /usr/local/apache2/conf/httpd-awstats.conf" >> /usr/local/apache2/conf/httpd.conf
#COPY httpd-awstats.conf /usr/local/apache2/conf/  # Loaded via ConfigMap in Kubernetes

# Enable Apache CGI Modules
RUN sed -i -e 's/#\(LoadModule cgi\)/\1/' /usr/local/apache2/conf/httpd.conf


##################################################
# Install AWStats
##################################################
ENV AWSTATS_VERSION=7.8
WORKDIR /usr/local/
RUN wget https://prdownloads.sourceforge.net/awstats/awstats-$AWSTATS_VERSION.tar.gz
RUN tar xvfz awstats-$AWSTATS_VERSION.tar.gz
RUN mv -v awstats-$AWSTATS_VERSION awstats
#COPY awstats.conf /etc/awstats/  # Loaded via ConfigMap in Kubernetes

# Apache runs as user "daemon"
RUN chown -R daemon:root /usr/local/awstats

# Redirect from "It Works" page to AWStats
COPY index.html /usr/local/apache2/htdocs/
