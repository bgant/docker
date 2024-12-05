# JSON data is piped into this script
# Example: ./rtl-433.sh | pipe-json.py

import sys
import json

# This module sends data to Webdis/Redis
from webdis import WEBDIS
webdis = WEBDIS()

# Create a generator function for piped JSON data 
def create_generator():
    for line in sys.stdin:
        if "time" in line:  # First field in any valid JSON reading is "time"
            yield json.loads(line)

def webdis_water_meter(id):
    webdis.timeseries(key=f"webdis-water-{id}-use",value=item['consumption'])
    webdis.timeseries(key=f"webdis-water-{id}-backflow",value=item['backflow'])
    webdis.timeseries(key=f"webdis-water-{id}-leak",value=item['leaknow'])

# Create generator object, access JSON data, and send to Webdis server
mygenerator = create_generator()
for item in mygenerator:  # item is just a dictionary
    if ("LaCrosse-TX29IT" in item['model']) and ("8" in str(item['id'])):  # My Front Porch Weather Sensor (old slim device)
        temp_F = (9 * float(item['temperature_C']))/5 + 32
        if item['battery_ok']:
            battery = 'OK'
        else:
            battery = 'Low'
        print(f"{item['model']} ID:{item['id']} {temp_F}\u00b0F and {item['humidity']}% humidity (battery {battery}) ")
        webdis.timeseries(key='webdis-porch-temp',value=temp_F)
        webdis.timeseries(key='webdis-porch-humidity',value=item['humidity'])
        webdis.timeseries(key='webdis-porch-battery',value=item['battery_ok'])
    elif ("LaCrosse-TX35DTHIT" in item['model']) and ("8" in str(item['id'])):  # My Porch Weather Sensor (duplicate data)
        pass
    elif "Neptune-R900" in item['model']:
        print(f"{item['model']} ID:{item['id']} Consumption:{item['consumption']} Backflow:{item['backflow']} LeakNow:{item['leaknow']}")
        webdis_water_meter(item['id'])
    else:
        print("Not Sent to Webdis: ", item)


# EXAMPLE rtl_433 json:
# {"time" : "2024-11-27 20:22:46", "model" : "LaCrosse-TX29IT", "id" : 8, "battery_ok" : 1, "newbattery" : 0, "temperature_C" : 5.300, "humidity" : 79, "mic" : "CRC"}
