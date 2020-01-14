# Source: https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx
# Source: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

FROM alpine:latest

WORKDIR /root

# Install APK Packages
RUN apk update && apk add --no-cache \
    bash \
    nginx \
    certbot \
    certbot-nginx

# Configure nginx
RUN mkdir /run/nginx && \
    mv /etc/nginx/conf.d/default.conf /root/default.conf
# Avoid creating logs in the container
# View logs with: docker service logs --follow main_nginx_app
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log 

# Copy over configuration files
COPY certbot_renew /etc/periodic/daily/
RUN chmod a+x /etc/periodic/daily/certbot_renew
COPY main-nginx.conf /etc/nginx/conf.d/main-nginx.conf
COPY EdgeX_architecture.png /var/lib/nginx/html/
COPY index.css /var/lib/nginx/html/
RUN mv /var/lib/nginx/html/index.html /var/lib/nginx/html/index.html.original
COPY index.html /var/lib/nginx/html/

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 
