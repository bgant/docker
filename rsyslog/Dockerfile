FROM alpine:3.12.0

RUN apk --no-cache update  \
    && apk add --no-cache \
    rsyslog

# Avoid container error messages about accessing /proc/kmsg kernel messages
RUN sed -i -e 's/\(module(load="imklog")\)/#\1/' /etc/rsyslog.conf

RUN mkdir /etc/rsyslog.d
COPY *.conf /etc/rsyslog.d/

WORKDIR /var/log

# Start rsyslod in interactive mode
CMD ["rsyslogd", "-n"]
