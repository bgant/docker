#!/bin/sh
# Usage: <script> [true|false]
# View available MQTT Topics using MQTT Explorer (AppImage)
/usr/bin/mosquitto_pub -h 172.17.0.1 -p 1883 -t 'zwave/Christmas_Tree/Power_Outlet/37/0/targetValue/set' -m "{\"value\":$1}"
