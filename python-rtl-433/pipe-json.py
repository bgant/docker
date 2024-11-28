import sys
import json

from webdis import WEBDIS
webdis = WEBDIS()

def create_generator():
    for line in sys.stdin:
        if "time" in line:
            #sys.stdout.write(line)
            yield json.loads(line)

mygenerator = create_generator()
for item in mygenerator:
    temp_F = (9 * float(item['temperature_C']))/5 + 32
    if item['battery_ok']:
        battery = 'OK'
    else:
        battery = 'Low'
    print(f"{item['model']} {temp_F}\u00b0F and {item['humidity']}% humidity (battery {battery}) ")
    webdis.timeseries(key='webdis-porch-temp',value=temp_F)
    webdis.timeseries(key='webdis-porch-humidity',value=item['humidity'])
    webdis.timeseries(key='webdis-porch-battery',value=item['battery_ok'])


# EXAMPLE rtl_433 json:
# {"time" : "2024-11-27 20:22:46", "model" : "LaCrosse-TX29IT", "id" : 8, "battery_ok" : 1, "newbattery" : 0, "temperature_C" : 5.300, "humidity" : 79, "mic" : "CRC"}
