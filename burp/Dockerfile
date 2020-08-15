# Source: https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx
# Source: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

FROM alpine:3.12.0

WORKDIR /root

# Install APK Packages
RUN apk update && apk add --no-cache \
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
    zlib-dev

# Clone uthash repo
RUN git clone https://github.com/troydhanson/uthash
RUN cp uthash/src/uthash.h /usr/include/

# Clone and Build Burp
RUN git clone https://github.com/grke/burp
WORKDIR /root/burp
RUN autoreconf -vif
RUN ./configure --prefix=/usr --sysconfdir=/etc/burp --localstatedir=/var
RUN make
RUN make install
RUN make install-configs

# Configure Burp:
#   Add Kubernetes ConfigMap for /etc/burp/burp-server.conf
#   Add Kubernetes Secret for /etc/burp/clientconfdir/
#   Add Kubernetes Certificates for /etc/burp/CA/burpserver.key, burpserver.crt (otherwise new server key with every build)
#    --OR--
#   Just backup /etc/burp/ files and mount as a persistent volume

# Data Volume:
#   Create /var/spool/burp/ persistent volume to hold backups

# Start Burp in foreground/stdout
CMD ["/usr/sbin/burp", "-vFc", "/etc/burp/burp-server.conf"] 
