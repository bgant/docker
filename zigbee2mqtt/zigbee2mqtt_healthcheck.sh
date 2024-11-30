#
# Docker healthcheck for https://www.zigbee2mqtt.io/
# See: https://github.com/Koenkk/zigbee2mqtt/issues/1310
# Source: https://gist.github.com/jbyers/5f0a279db8b0022251eb699ee3db5305/
#
# Requires `apk add mosquitto-clients`
#
# In Docker healthcheck, run as `ash /path/to/healthcheck.sh || exit 1`
#
set -e

MQTT_HOST="mqtt"
TIMEOUT_SECONDS="5"

TMPFILE=`mktemp`
trap "rm -f $TMPFILE" 0

mosquitto_sub \
  -h $MQTT_HOST \
  -t zigbee2mqtt/bridge/response/health_check \
  -C 1 -N -W $TIMEOUT_SECONDS \
  > $TMPFILE 2>&1 &

mosquitto_pub \
  -h $MQTT_HOST \
  -t zigbee2mqtt/bridge/request/health_check \
  -n

# mosquitto_sub will either exit instantly having received
# the reponse (-C 1) or will time out (-W $TIMEOUT_SECONDS)
wait

# yuck
grep -q '{"data":{"healthy":true},"status":"ok"}' $TMPFILE
