#!/bin/bash
#
# apk add mosquitto-clients
#
# crontab -l
# 00     16       *       *       *       /root/source/bgant/tools/alpine-zfs-docker/zigbee2mqtt/restart_zigbee2mqtt.sh
# 10     16       *       *       *       /root/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto/light_control.py
# 01     21       *       *       *       /root/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto/light_control.py
# 00     22       *       *       *       /root/source/bgant/tools/alpine-zfs-docker/eclipse-mosquitto/light_control.py

echo "Sending Request to Turn Lights Off..."
mosquitto_pub -h 172.17.0.1 -p 1883 -t 'zigbee2mqtt/FrontOutsideLights/set' -m '{ "state": "OFF" }'
echo "Waiting 30 seconds for any errors..."
sleep 30
if [ `docker logs --since 2m zigbee2mqtt | grep -c Error` != 0 ]
then 
   echo "Errors Found in Logs... Restarting Container..."
   docker restart zigbee2mqtt
else
   echo "No Errors in Logs... Exiting"
fi

