 #!/usr/bin/python3
#

from RPi import GPIO
import time

class RGBLEDStrip:

  def __init__(self, pin_r, pin_g, pin_b):
    self.r = pin_r
    self.g = pin_g
    self.b = pin_b
    self.dc_r = 0
    self.dc_g = 0
    self.dc_b = 0
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

  def setColor(self, color):
    self.setDC( color["r"] * 100, color["g"] * 100, color["b"] * 100 )

  def configPWM(self, freq=100):
    self.pwm_r = GPIO.PWM(self.r, freq)
    self.pwm_g = GPIO.PWM(self.g, freq)
    self.pwm_b = GPIO.PWM(self.b, freq)
    self.pwm_r.start(self.dc_r)
    self.pwm_g.start(self.dc_g)
    self.pwm_b.start(self.dc_b)

  def setDC(self, dc_r, dc_g, dc_b):
    print("setDC", dc_r, dc_g, dc_b)
    self.dc_r = dc_r
    self.dc_g = dc_g
    self.dc_b = dc_b
    self.pwm_r.ChangeDutyCycle(self.dc_r)
    self.pwm_g.ChangeDutyCycle(self.dc_g)
    self.pwm_b.ChangeDutyCycle(self.dc_b)

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
        time.sleep(0.02)
      for dc in range(100, -1, -5):
        leds.setDC(dc, dc, dc)
        time.sleep(0.02)

  except KeyboardInterrupt:
    pass

  leds.off()
  GPIO.cleanup()
