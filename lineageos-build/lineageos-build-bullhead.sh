#!/bin/bash

# Source: https://wiki.lineageos.org/devices/bullhead/build

cd /root/android/lineage
/usr/local/bin/repo init -u https://github.com/LineageOS/android.git -b lineage-17.1

repo sync
