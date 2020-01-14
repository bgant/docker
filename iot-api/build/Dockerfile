# Source: https://pythonforundergradengineers.com/flask-app-on-digital-ocean.html
# Source: https://netdevops.me/2017/flask-application-in-a-production-ready-container/
# Source: https://github.com/hellt/nginx-uwsgi-flask-alpine-docker/tree/master/python3

FROM alpine:latest

WORKDIR /opt

# Install APK Packages
RUN apk update && apk add --no-cache \
    python3 \
    bash \
    nginx \
    uwsgi \
    uwsgi-python \
    py3-tz \
    supervisor

# Update pip and install packages
COPY requirements.txt .
RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt

# Configure nginx
RUN rm /etc/nginx/conf.d/default.conf && \
    mkdir /run/nginx && \
    rm -r /root/.cache
# Avoid creating logs in the container
# View logs with: docker service logs --follow iot-api_app
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log 

# Create database directory
RUN mkdir /opt/data && chown nginx:nginx /opt/data && chmod 770 /opt/data

# Install self-signed openssl files (create with generate-openssl.sh)
#COPY localhost.crt /etc/ssl/certs/localhost.crt 
#COPY localhost.key /etc/ssl/private/localhost.key 

# Copy over configuration files
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/
COPY flaskapp.py .
COPY static/ ./static/
COPY templates/ ./templates/
COPY authenticate.py .

#CMD ["python", "/root/flaskapp.py"]
#CMD uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
#CMD ["nginx", "-g", "daemon off;"] 
CMD ["/usr/bin/supervisord"]
