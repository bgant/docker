#!/bin/bash
#
# This script assumes Dockerfile has already install the following packages:
#   apk add bash html-xml-utils

# lighttpd web server
dir="/var/www/localhost/htdocs"
user="lighttpd"

# nginx web server
#dir="/var/www/html"
#user="www-data"

# Find the latest version number (major.minor.patch) of mediawiki for download
major=$(wget -q -O - http://releases.wikimedia.org/mediawiki/ | \
                hxnormalize -x | hxselect -c -s '\n' a | grep ^'1.' | grep -v rc | \
                awk -F'/' '{print $1}' | awk -F'.' '{print $1}' | sort -n | tail -n 1)

minor=$(wget -q -O - http://releases.wikimedia.org/mediawiki/ | \
                hxnormalize -x | hxselect -c -s '\n' a | grep ^'1.' | grep -v rc | \
                awk -F'/' '{print $1}' | awk -F'.' '{print $2}' | sort -n | tail -n 1)

patch=$(wget -q -O - http://releases.wikimedia.org/mediawiki/${major}.${minor}/ | \
                hxnormalize -x | hxselect -c -s '\n' a | \
                grep mediawiki-${major}.${minor} | grep -v rc | \
                awk -F'.' '{print $3}' | sort -n | tail -n 1)

echo "Latest mediawiki version: ${major}.${minor}.${patch}"

# Assuming nginx is the web server
wget -O ${dir}/mediawiki-${major}.${minor}.${patch}.tar.gz http://releases.wikimedia.org/mediawiki/${major}.${minor}/mediawiki-${major}.${minor}.${patch}.tar.gz
tar xvfz ${dir}/mediawiki-${major}.${minor}.${patch}.tar.gz -C ${dir}/
rm ${dir}/mediawiki-${major}.${minor}.${patch}.tar.gz
ln -s ${dir}/mediawiki-${major}.${minor}.${patch} ${dir}/mediawiki
chown -R ${user} ${dir}

