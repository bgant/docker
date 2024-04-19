# cd ~/source/bgant/docker/alpine-compile/aide
# docker build . -t alpine-compile-aide
# docker run --rm -it alpine-compile-aide /bin/sh  <-- If needed
# <see AIDE setup instructions at the end of this file>

FROM alpine:3.18.6

WORKDIR /root

# Install git and download AIDE
RUN apk update && apk add --no-cache git
RUN git clone https://github.com/aide/aide

# Install packages for compiling AIDE
RUN apk add --no-cache \
    coreutils \
    gcc \
    g++ \
    automake \
    autoconf \
    flex \
    bison \
    make \
    pkgconfig \
    pcre2-dev \
    check-dev \
    libgcrypt-dev \
    mandoc

# sh ./autogen.sh -f doesn't work
WORKDIR /root/aide
RUN sed -i 's/-fv/-v/g' autogen.sh
RUN sh ./version.sh
RUN autoreconf -v --install || :  # Fails the first time (|| : ignores exit code)
RUN autoreconf -v --install

# Running ./configure
RUN sed -i 's/AX_PTHREAD/#AX_PTHREAD/g' configure
RUN ./configure

# Run make
RUN make
RUN make check
RUN make install
RUN aide --version | grep AIDE

# Files installed are:
# /usr/local/bin/aide
# /usr/local/share/man/man1
# /usr/local/share/man/man5
#
# Manual files:
# man aide
# man aide.conf
#
# Copy files to host:
# docker cp alpine-compile-aide:/usr/local/bin/aide /usr/local/bin/
#
# Copy aide.conf:
# mkdir /usr/local/etc
# cp aide.conf /usr/local/etc/
# aide --config-check
#
# Initialize AIDE:
# mkdir /var/lib/aide
# nice -19 aide --init && mv -v /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
#
# Run AIDE check:
# nice -19 aide --check
# crontab -e
#   00 05 * * * nice -19 aide --check | tac | sed '2,27d' | tac > /var/log/aide-check.log
#
# Reset AIDE update after known SysAdmin changes:
# nice -19 aide --update && mv -v /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz

