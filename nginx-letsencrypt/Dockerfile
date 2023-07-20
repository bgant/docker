# Source: https://ilhicas.com/2019/03/02/Nginx-Letsencrypt-Docker.html

# git pull
# vi Dockerfile
# < change FROM to latest version found at https://hub.docker.com >
# docker compose build
# docker tag <name>:latest registry.localdomain:5000/<name>:<year-month-day>
# docker push registry.localdomain:5000/<name>:<year-month-day>
# < edit Kubernetes Docker Image to registry.localdomain:5000/<name>:<year-month-day> >
# git add Dockerfile
# git commit -m "<new image name>"
# git push

FROM nginx:1.25.1-alpine

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
