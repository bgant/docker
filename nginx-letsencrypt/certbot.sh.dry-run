#!/bin/sh
#
# Source: https://ilhicas.com/2019/03/02/Nginx-Letsencrypt-Docker.html
#

### Directory for HTTP Port 80 /.well-known/acme-challenge/ requests
if [[ ! -f /var/www/certbot ]]; then
    mkdir -p /var/www/certbot
fi

### Check to see if certificates should be renewed
certbot certonly \
        --config-dir "${LETSENCRYPT_DIR:-/etc/letsencrypt}" \
                --dry-run \
		--agree-tos \
		--domains "${DOMAIN:?NeedDomainEnvironmentVariable}" \
		--email "${EMAIL:?NeedEmailEnvironmentVariable}" \
		--expand \
		--noninteractive \
		--webroot \
		--webroot-path /var/www/certbot \
		$OPTIONS || true

### Copy certificates (renewed or not) over for nginx to use
if [[ -f "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/$DOMAIN/privkey.pem" ]]; then
    cp "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/$DOMAIN/privkey.pem" /usr/share/nginx/certificates/privkey.pem
    cp "${LETSENCRYPT_DIR:-/etc/letsencrypt}/live/$DOMAIN/fullchain.pem" /usr/share/nginx/certificates/fullchain.pem
fi

