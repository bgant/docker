#!/bin/bash
#
# This script requires tools from the html-xml-utils package (hxnormalize and hxselect)

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

if [ ! -e mediawiki-${major}.${minor}.${patch}.tar.gz ]
then
    wget -O mediawiki-${major}.${minor}.${patch}.tar.gz http://releases.wikimedia.org/mediawiki/${major}.${minor}/mediawiki-${major}.${minor}.${patch}.tar.gz
fi
echo "extracting files from mediawiki-${major}.${minor}.${patch}.tar.gz..."
tar xfz mediawiki-${major}.${minor}.${patch}.tar.gz
#rm mediawiki-${major}.${minor}.${patch}.tar.gz

