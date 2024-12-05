#!/bin/sh
# -s 250K is the sampling rate
# -R 76 only listens for LaCrosse TX29IT
#rtl_433 -f 915M -s 250K -R 76 -F json

# -f 915MHz is LaCrosse weather devices
# -f 912MHz is Neptune-R900 Water Meters                         
# -f 912MHz listens again for Water Meters (915MHz 1/3 of time and 912MHz 2/3 of time)
# -H 17 hops every 17 seconds between the two frequencies
#    (LaCrosse is every 36s and water meters every 160s / odd number of seconds that is half LaCrosse)
# -E hop switches immediately to the next frequency when a message is logged
# -Y autolevel adjusts the interference sensitivity of the device automatically
# -F json outputs in JSON format
rtl_433 -f 915M -f 912M -f 912M -H 17 -E hop -Y autolevel -F json
