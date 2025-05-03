#!/bin/sh
#
# Check every 2 minutes:
# crontab -l 
# */2     *       *       *       *       /root/source/bgant/docker/python-rtl-433/check_rtl.sh

if [ `podman logs --since 2m python-rtl-433 | grep -c 'usb_open error'` != 0 ]
then 
   echo "Errors Found in python-rtl-433 logs... Recreating Container..."
   echo -n "Stopping container: "
   podman stop python-rtl-433
   sleep 2
   echo -n "Removing container: "
   podman rm python-rtl-433
   sleep 2
   echo "Reloading udevadm rules..."
   udevadm control --reload-rules && udevadm trigger
   sleep 2
   echo -n "Creating new python-rtl-433 container: "
   podman run -d --name python-rtl-433 --restart always --device=/dev/bus/usb:/dev/bus/usb localhost/python-rtl-433:latest
   echo "Done"
else
   echo "No Errors in python-rtl-433 logs... Exiting"
fi

