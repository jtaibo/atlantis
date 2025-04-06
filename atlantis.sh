#!/bin/bash
#

if [ `id -u` != 0 ]; then
  SUDO=sudo
fi

# Disable power saving for the WiFi interface, so it is always available to connect
# atlantis host through the network
$SUDO iw dev wlan0 set power_save off

cd `dirname $0`
./atlantis.py
