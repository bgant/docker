#!/bin/sh
# Source: https://github.com/merbanan/rtl_433/blob/master/docs/INTEGRATION.md
rtl_433 -f 915M -R 76 -s 250K -F "influx://${INFLUXDB_HOST}:${INFLUXDB_PORT}/write?db=${INFLUXDB_DATABASE}&u=${INFLUXDB_USERNAME}&p=${INFLUXDB_PASSWORD}" -M time:unix:usec:utc
