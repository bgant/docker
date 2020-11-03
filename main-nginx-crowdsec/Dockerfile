# Source: https://github.com/crowdsecurity/cs-nginx-blocker#installation
# Source: https://github.com/crowdsecurity/crowdsec
#FROM nginx:1.19.3-alpine
FROM alpine:3.12.1

WORKDIR /opt/

RUN apk update && apk add --no-cache git bash gettext newt curl wget make jq go nginx

RUN mkdir -p /run/nginx
RUN mkdir /etc/cron.d

RUN git clone https://github.com/crowdsecurity/crowdsec
RUN cd crowdsec; make build
RUN sed -i 's/ -ctime -5//g' crowdsec/wizard.sh
RUN cd crowdsec; nginx; ./wizard.sh --unattended
RUN cscli install collection crowdsecurity/nginx
#RUN echo -e "load_module /usr/lib/nginx/modules/ndk_http_module.so;\nload_module /usr/lib/nginx/modules/ngx_http_lua_module.so;\n$(cat /etc/nginx/nginx.conf)" > /etc/nginx/nginx.conf

# Install cs-nginx-blocker
RUN apk update && apk add --no-cache lua5.3 nginx-mod-http-lua lua-sql-sqlite3 lua-sql-mysql lua-resty-core
RUN git clone https://github.com/crowdsecurity/cs-lua-lib.git
RUN git clone https://github.com/crowdsecurity/cs-nginx-blocker.git
RUN cp cs-nginx-blocker/nginx/crowdsec_nginx.conf /etc/nginx/conf.d/crowdsec_nginx.conf
RUN mkdir -p /usr/local/lua/crowdsec
RUN cp cs-lua-lib/lib/*.lua /usr/local/lua/crowdsec/
RUN cp cs-nginx-blocker/nginx/access.lua /usr/local/lua/crowdsec/

# Add OpenResty for nginx: https://openresty.org/en/linux-packages.html
#RUN cd /etc/apk/keys; wget 'http://openresty.org/package/admin@openresty.com-5ea678a6.rsa.pub'
#RUN . /etc/os-release; MAJOR_VER=`echo $VERSION_ID | sed 's/\.[0-9]\+$//'`; echo "http://openresty.org/package/alpine/v$MAJOR_VER/main" | tee -a /etc/apk/repositories
#RUN apk update && apk add --no-cache openresty
#RUN rm /usr/bin/luajit; ln -s /usr/local/openresty/luajit/bin/luajit /usr/bin/luajit


RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
CMD ["nginx", "-g", "daemon off;"]
