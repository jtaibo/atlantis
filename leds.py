#!/usr/bin/python3
#

from RPi import GPIO
import time

class RGBLEDStrip:

  def __init__(self, pin_r, pin_g, pin_b):
    self.r = pin_r
    self.g = pin_g
    self.b = pin_b
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.r, GPIO.OUT) # R
    GPIO.setup(self.g, GPIO.OUT) # G
    GPIO.setup(self.b, GPIO.OUT) # B

  def on(self):
    GPIO.output(self.r, 1)
    GPIO.output(self.g, 1)
    GPIO.output(self.b, 1)

  def off(self):
    GPIO.output(self.r, 0)
    GPIO.output(self.g, 0)
    GPIO.output(self.b, 0)

  def configPWM(self, freq=100, dc=50):
    self.pwm_r = GPIO.PWM(self.r, freq)
    self.pwm_g = GPIO.PWM(self.g, freq)
    self.pwm_b = GPIO.PWM(self.b, freq)
    self.pwm_r.start(dc)
    self.pwm_g.start(dc)
    self.pwm_b.start(dc)

  def setDC(self, dc_r, dc_g, dc_b):
    self.pwm_r.ChangeDutyCycle(dc_r)
    self.pwm_g.ChangeDutyCycle(dc_g)
    self.pwm_b.ChangeDutyCycle(dc_b)

  def stopPWM(self):
    self.pwm_r.stop()
    self.pwm_g.stop()
    self.pwm_b.stop()


if __name__ == '__main__':     # Testing code

  leds = RGBLEDStrip(25, 24, 23)
  leds.configPWM()
  
  leds.on()
  time.sleep(1)
  leds.off()
  time.sleep(1)

  try:
    while True:
      for dc in range(0, 101, 5):
        leds.setDC(dc, dc, dc)
        time.sleep(0.1)
      for dc in range(100, -1, -5):
        leds.setDC(dc, dc, dc)
        time.sleep(0.1)

  except KeyboardInterrupt:
    pass

  GPIO.cleanup()
