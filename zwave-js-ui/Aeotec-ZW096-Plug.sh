#!/bin/sh
#
# apk add mosquitto-clients
#
# Usage: <script> [true|false]
#
# View available MQTT Topics using MQTT Explorer (AppImage)
# Whatever Name and Location you create for the device is what is used to connect to the device

if [[ -z $1 ]]; then
    echo "Requires Paramater: [true|false]"
else
    /usr/bin/mosquitto_pub -h 192.168.7.140 -p 1883 -t 'zwave/zwave-plug/37/0/targetValue/set' -m "{\"value\":$1}"
fi
