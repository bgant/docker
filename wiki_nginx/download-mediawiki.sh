#!/bin/bash
#
# This script assumes Dockerfile has already install the following packages:
#   apk add bash html-xml-utils

# lighttpd web server
#dir="/var/www/localhost/htdocs"
#user="lighttpd"

# nginx web server
dir="/var/www/localhost/htdocs"
user="nginx"

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

# For when a new release candidate is first released
if [ -n patch ]
then
    minor=$(($minor - 1))
    patch=$(wget -q -O - http://releases.wikimedia.org/mediawiki/${major}.${minor}/ | \
                hxnormalize -x | hxselect -c -s '\n' a | \
                grep mediawiki-${major}.${minor} | grep -v rc | \
                awk -F'.' '{print $3}' | sort -n | tail -n 1)
fi

echo "Latest mediawiki version: ${major}.${minor}.${patch}  (excluding release candidates)"

# Assuming nginx is the web server
wget -O ${dir}/mediawiki-${major}.${minor}.${patch}.tar.gz http://releases.wikimedia.org/mediawiki/${major}.${minor}/mediawiki-${major}.${minor}.${patch}.tar.gz
tar xfz ${dir}/mediawiki-${major}.${minor}.${patch}.tar.gz -C ${dir}/
rm ${dir}/mediawiki-${major}.${minor}.${patch}.tar.gz
cd ${dir}
ln -s mediawiki-${major}.${minor}.${patch} mediawiki
chown -R ${user}:${user} ${dir}

