#!/bin/bash
#

if [ `id -u` != 0 ]; then
  SUDO=sudo
fi

$SUDO iw dev wlan0 set power_save off

cd `dirname $0`
./atlantis.py
