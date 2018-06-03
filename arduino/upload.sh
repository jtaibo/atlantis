#!/bin/bash
#

PORT=/dev/ttyUSB0
#VERBOSE=--verbose-upload
VERBOSE=
BOARD=arduino:avr:nano:cpu=atmega328
ARDUINO=/home/pi/arduino-1.8.5/arduino

if [ $# -lt 1 ]; then
  echo "Syntax: $0 <program.ino>"
  exit 1
fi

# One-time configuration
#    to-do: check whether they are installed or not
#$ARDUINO --install-boards "arduino:avr"

#$ARDUINO $VERBOSE --port $PORT --verify blink.ino
$ARDUINO $VERBOSE --board $BOARD --port $PORT --upload $1
