#!/usr/bin/python3
#

import serial

baud_rate = 9600
ser = serial.Serial("/dev/ttyUSB0", baud_rate)

try:
  while True:
    read_serial = ser.readline()
#    print("Received: ", read_serial)
    print( read_serial.decode("ascii") )

except KeyboardInterrupt:
  pass

finally:
  pass
