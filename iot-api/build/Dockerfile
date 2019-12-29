# Source: https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html
# Source: https://netdevops.me/2017/flask-application-in-a-production-ready-container/
# Source: https://github.com/hellt/nginx-uwsgi-flask-alpine-docker/tree/master/python3

FROM alpine:latest

WORKDIR /opt                                         
COPY requirements.txt .

RUN apk add --no-cache \
    python3 \
    bash \
    nginx \
    uwsgi \
    uwsgi-python \
    py3-requests \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt && \
    rm /etc/nginx/conf.d/default.conf && \
    mkdir /run/nginx && \
    rm -r /root/.cache

#COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/
COPY flaskapp.py .
COPY authenticate.py .

# Install self-signed openssl files (create with generate-openssl.sh)
# --OR--
# Install Let's Encrypt Certificates
#    sudo add-apt-repository ppa:certbot/certbot
#    sudo apt install python-certbot-nginx
#    sudo certbot --nginx -d mydomain.com -d www.mydomain.com
#COPY localhost.crt /etc/ssl/certs/localhost.crt
#COPY localhost.key /etc/ssl/private/localhost.key

# Make network port available
#EXPOSE 80

# From nginx Dockerfile
# Source: https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile
# Forward request and error logs to docker log collector
#RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
#    ln -sf /dev/stderr /var/log/nginx/error.log
#CMD ["nginx", "-g", "daemon off;"]
#CMD ["python", "/root/flaskapp.py"]
#CMD uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
CMD ["/usr/bin/supervisord"]
