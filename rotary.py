#!/usr/bin/python3
#

import RPi.GPIO as GPIO
from globalconfig import GlobalConfig
import time


class RotaryEncoder:

  def __init__(self, clk_pin=GlobalConfig.rotary_clk_pin, dt_pin=GlobalConfig.rotary_dt_pin, sw_pin=GlobalConfig.rotary_sw_pin):
    self.RoAPin = dt_pin
    self.RoBPin = clk_pin
    self.sw_pin = sw_pin
    self.counter = 0        # Accumulated rotation
    self.new_click = False	# New click detected
    self.rotate_ts = 0      # Last rotation timestamp
    self.click_ts = 0       # Last click timestamp
    GPIO.setmode(GPIO.BCM)         # Numbers GPIOs by Broadcom SOC channel, not physical pin location
    GPIO.setup(self.RoAPin, GPIO.IN)
    GPIO.setup(self.RoBPin, GPIO.IN)
    GPIO.setup(self.sw_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    # Detect rotations
    GPIO.add_event_detect(self.RoAPin, GPIO.FALLING, callback=self.fall_a, bouncetime=100)
    # Detect clicks
    GPIO.add_event_detect(self.sw_pin, GPIO.FALLING, callback=self.click, bouncetime=200) # wait for falling

  def fall_a(self, channel):
    self.rotate_ts = time.time()
    if ( GPIO.input(self.RoBPin) == GPIO.LOW ):
      self.counter = self.counter + 1
    else:
      self.counter = self.counter - 1

  def click(self, channel):
    self.new_click = True
    self.click_ts = time.time()

  def getCounter(self):
    return self.counter

  def getNewClick(self):
    nc = self.new_click
    self.new_click = False
    return nc
        
  def getLastRotationTS(self):
    return self.rotate_ts
        
  def getLastClickTS(self):
    return self.click_ts

  def getLastInteractionTS(self):
    return max( self.getLastClickTS(), self.getLastRotationTS() )

  def getLastRotationDelta(self):
    return time.time() - self.rotate_ts

  def getLastClickDelta(self):
    return time.time() - self.click_ts

  def getLastIterationDelta(self):
    return time.time() - self.getLastInteractionTS()

if __name__ == '__main__':     # Testing code

  re = RotaryEncoder()
  while True:
    time.sleep(.1)
    print( "counter = " + str(re.getCounter()) )
#    print( "time = " + str(time.time()))
#    print("Last click " + str(time.time() - re.getLastClickTS()) + " seconds ago")
#    print("Last rotation " + str(time.time() - re.getLastRotationTS()) + " seconds ago")
    print("Last interaction was " + str(time.time() - re.getLastInteractionTS()) + " seconds ago")
