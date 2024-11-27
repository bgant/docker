#!/bin/sh

# https://github.com/troydhanson/uthash/tags
UTHASH="v2.3.0"

# https://github.com/grke/burp/tags
BURP="2.5.4"

mkdir /root/burp-build
cd /root/burp-build

# Install APK Packages
#   Search for specific missing files at https://pkgs.alpinelinux.org/contents
apk update && apk add \
    bash \
    git \
    build-base \
    gcc \
    make \
    pkgconf \
    autoconf \
    automake \
    libtool \
    librsync \
    librsync-dev \
    openssl \
    openssl-dev \
    zlib-dev \
    linux-headers \
    bsd-compat-headers

# Get git repos for uthash and burp
git config --global advice.detachedHead false

git clone --depth 1 --branch $UTHASH  https://github.com/troydhanson/uthash
cp uthash/src/uthash.h /usr/include/

git clone --depth 1 --branch $BURP https://github.com/grke/burp
cd /root/burp-build/burp
autoreconf -vif
./configure --prefix=/usr --sysconfdir=/etc/burp --localstatedir=/var
make
make install
make install-configs
