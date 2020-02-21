# Source: https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx
# Source: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

FROM alpine:latest

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

# Configure Burp
#   Add Kubernetes ConfigMap for /etc/burp/burp-server.conf
#   Add Kubernetes Secret for /etc/burp/clientconfdir/
#RUN ln -sf /dev/stdout /var/log/nginx/access.log \
#    && ln -sf /dev/stderr /var/log/nginx/error.log 

# Start Burp in foreground/stdout
CMD ["/usr/sbin/burp", "-vFc", "/etc/burp/burp-server.conf"] 
