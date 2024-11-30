FROM koenkk/zigbee2mqtt:1.38.0
RUN apk update && apk add --no-cache mosquitto-clients
COPY zigbee2mqtt_healthcheck.sh ./

# docker build -t zigbee2mqtt-healthcheck .

