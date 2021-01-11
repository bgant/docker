#!/usr/bin/env python
# Source: https://github.com/merbanan/rtl_433/tree/master/examples/rtl_433_influxdb_relay.py

"""InfluxDB monitoring relay for rtl_433."""

# Setup Instructions:
#   apt-get install rtl_433 python3-influxdb python3-daemon
#
#   curl -G "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "q=SHOW DATABASES"
#   curl -XPOST 'http://influxdb.localdomain:8086/query' --data-urlencode 'q=CREATE DATABASE "rtl433"'
#
#   rtl_433 -f 915M -R 76 -F syslog::1433 -vv &
#   tcpdump -i lo -nnvv -X port 1433
#
#   python3 rtl_433_influxdb_relay.py
#   curl -G "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "db=rtl433" --data-urlencode "q=SHOW FIELD KEYS"
#   curl -G "http://influxdb.localdomain:8086/query?pretty=true" --data-urlencode "db=rtl433" --data-urlencode 'q=SELECT * FROM "LaCrosse-TX29IT" ORDER BY DESC LIMIT 3'
#
#   cp rc-local.service /etc/systemd/system/
#   cp rc.local /etc/
#   chmod +x /etc/rc.local
#   systemctl enable rc-local
#   reboot
 

# Option: PEP 3143 - Standard daemon process library
# (use Python 3.x or pip install python-daemon)
# import daemon

from __future__ import print_function
from __future__ import with_statement

from influxdb import InfluxDBClient
import socket
from datetime import datetime
import json
import sys

from os import environ
UDP_IP = "127.0.0.1"
UDP_PORT = 1433
INFLUXDB_HOST = environ['INFLUXDB_HOST']
INFLUXDB_PORT = environ['INFLUXDB_PORT']
INFLUXDB_USERNAME = environ['INFLUXDB_USERNAME']
INFLUXDB_PASSWORD = environ['INFLUXDB_PASSWORD']
INFLUXDB_DATABASE = environ['INFLUXDB_DATABASE']

TAGS = [
    "channel",
    "id",
]

FIELDS = [
    "temperature_C",
    "humidity",
    "battery_ok",
    "pressure_hPa",
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.bind((UDP_IP, UDP_PORT))


def sanitize(text):
    return text.replace(" ", "_").replace("/", "_").replace(".", "_").replace("&", "")


def parse_syslog(line):
    """Try to extract the payload from a syslog line."""
    line = line.decode("ascii")  # also UTF-8 if BOM
    if line.startswith("<"):
        # fields should be "<PRI>VER", timestamp, hostname, command, pid, mid, sdata, payload
        fields = line.split(None, 7)
        line = fields[-1]
    return line


def rtl_433_probe():
    client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT,
                            username=INFLUXDB_USERNAME, password=INFLUXDB_PASSWORD,
                            database=INFLUXDB_DATABASE)

    while True:
        line, _addr = sock.recvfrom(1024)

        try:
            line = parse_syslog(line)
            data = json.loads(line)

            if not "model" in data:
                continue
            measurement = sanitize(data["model"])

            tags = {}
            for tag in TAGS:
                if tag in data:
                    tags[tag] = data[tag]

            fields = {}
            for field in FIELDS:
                if field in data:
                    if field == 'temperature_C' or field == 'pressure_hPa':
                        fields[field] = float(data[field])
                    else:
                        fields[field] = int(data[field])
                    #print(field, fields[field], type(fields[field]))

            if len(fields) == 0:
                continue

            point = {
                "measurement": measurement,
                "time": datetime.utcnow().isoformat(),
                "tags": tags,
                "fields": fields,
            }

            try:
                print(point)
                client.write_points([point])
            except Exception as e:
                print("error {} writing {}".format(e, point), file=sys.stderr)

        except KeyError:
            pass

        except ValueError:
            pass


def run():
    # with daemon.DaemonContext(files_preserve=[sock]):
    #  detach_process=True
    #  uid
    #  gid
    #  working_directory
    rtl_433_probe()


if __name__ == "__main__":
    run()
