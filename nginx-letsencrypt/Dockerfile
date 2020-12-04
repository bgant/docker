# Source: https://ilhicas.com/2019/03/02/Nginx-Letsencrypt-Docker.html

FROM nginx:1.19.5-alpine

WORKDIR /root

# Install APK Packages
RUN apk update && apk add --no-cache \
    bash \
    certbot \
    certbot-nginx \
    inotify-tools \
    openssl

COPY entrypoint.sh entrypoint.sh
COPY certbot.sh certbot.sh
COPY minimal-nginx.conf /etc/nginx/conf.d/default.conf
RUN chmod +x entrypoint.sh && \
    chmod +x certbot.sh 
ENTRYPOINT ["./entrypoint.sh"]
