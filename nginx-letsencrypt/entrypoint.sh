#!/bin/sh
#
# Source: https://ilhicas.com/2019/03/02/Nginx-Letsencrypt-Docker.html
#

### Ensure we have folders available
if [[ ! -f /usr/share/nginx/certificates/fullchain.pem ]];then
    mkdir -p /usr/share/nginx/certificates
fi

### If certificates already exist copy them over for nginx to use
if [[ -f "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/${DOMAIN:?NeedDomainEnvironmentVariable}/privkey.pem" ]]; then
    cp "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/$DOMAIN/privkey.pem" /usr/share/nginx/certificates/privkey.pem
    cp "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/$DOMAIN/fullchain.pem" /usr/share/nginx/certificates/fullchain.pem
fi

### If certificates do not exist create them to start nginx
if [[ ! -f /usr/share/nginx/certificates/fullchain.pem ]]; then
    openssl genrsa -out /usr/share/nginx/certificates/privkey.pem 4096
    openssl req -new \
        -key /usr/share/nginx/certificates/privkey.pem \
        -out /usr/share/nginx/certificates/cert.csr -nodes -subj \
        "/C=US/ST=World/O=Temporary/CN=${DOMAIN}"
    openssl x509 -req -days 365 \
        -in /usr/share/nginx/certificates/cert.csr \
        -signkey /usr/share/nginx/certificates/privkey.pem \
        -out /usr/share/nginx/certificates/fullchain.pem
fi

### Send certbot Emission/Renewal to background
$(while :; do ./certbot.sh; sleep "${RENEW_INTERVAL:-12h}"; done;) &

### Check for changes in the certificate (i.e renewals or first start) and send this process to background
$(while inotifywait -e close_write /usr/share/nginx/certificates; do nginx -s reload; done) &

### Start nginx with daemon off as our main pid
nginx -g "daemon off;"

