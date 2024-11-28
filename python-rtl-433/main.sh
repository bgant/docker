#!/bin/sh
./rtl-433.sh | python3 -u pipe-json.py

# docker logs not showing python print? Need -u for unbuffered output
# Source: http://stackoverflow.com/questions/29663459/ddg#29745541
