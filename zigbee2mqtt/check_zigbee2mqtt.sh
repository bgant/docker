#!/bin/sh
#
# apk add mosquitto-clients
#
# crontab -l
# 00     16       *       *       *       /root/source/bgant/docker/zigbee2mqtt/restart_zigbee2mqtt.sh
# 10     16       *       *       *       /root/source/bgant/docker/eclipse-mosquitto/light_control.sh
# 01     21       *       *       *       /root/source/bgant/docker/eclipse-mosquitto/light_control.sh
# 00     22       *       *       *       /root/source/bgant/docker/eclipse-mosquitto/light_control.sh

echo "Sending Request to Turn Lights Off..."
mosquitto_pub -h 10.88.0.1 -p 1883 -t 'zigbee2mqtt/FrontOutsideLights/set' -m '{ "state": "OFF" }'
echo "Waiting 30 seconds for any errors..."
sleep 30
if [ `podman logs --since 2m zigbee2mqtt | grep -c Error` != 0 ]
then 
   echo "Errors Found in Logs... Restarting Container..."
   podman restart zigbee2mqtt
else
   echo "No Errors in Logs... Exiting"
fi

