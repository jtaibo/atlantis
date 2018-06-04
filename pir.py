#!/usr/bin/python3
#

from RPi import GPIO
from globalconfig import GlobalConfig
import time

class PIR:
  def __init__(self):
    self.pin = GlobalConfig.pir_pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pin, GPIO.IN)
  
  def detection(self):
    return GPIO.input( self.pin ) == 1

if __name__ == '__main__':     # Testing code

  try:

    pir = PIR()
    while True:
      if pir.detection():
        print("DETECTION")
      else:
        print("NO DETECTION")
      time.sleep(0.1)

  except KeyboardInterrupt:
    pass

  finally:
    pass
