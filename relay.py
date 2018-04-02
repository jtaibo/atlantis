#!/usr/bin/python3
#

import RPi.GPIO as GPIO

class RelayDevice:
  def __init__(self, name, ch, idx):
    self.name = name  # device unique id
    self.channel = ch # physical channel in the relay module
    self.idx = idx    # device index (used to sort devices)


class RelayModule:

  def __init__(self, relay_pins):
    self.relay_pins = relay_pins
    self.devices = {}
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by Broadcom SOC channel (GPIO #, not pin #)
    GPIO.setup(self.relay_pins, GPIO.OUT, initial=GPIO.HIGH)

  def on(self, ch):
    GPIO.output(self.relay_pins[ch], GPIO.LOW)

  def off(self, ch):
    GPIO.output(self.relay_pins[ch], GPIO.HIGH)

  def toggle(self, ch):
    GPIO.output(self.relay_pins[ch], 1-GPIO.input(self.relay_pins[ch]))

  def size(self):
    return len(self.relay_pins)

  def getState(self, ch):
    # NOTE: Logic value is inverted
    return 1-GPIO.input(self.relay_pins[ch])

  # API for named devices

  def registerDevice(self, name, ch):
    self.devices[name] = RelayDevice(name, ch, len(self.devices))

  def turnOnDevice(self, name):
    if name in self.devices:
      self.on( self.devices[name].channel )

  def turnOffDevice(self, name):
    if name in self.devices:
      self.off( self.devices[name].channel )

  def toggleDevice(self, name):
    if name in self.devices:
      self.toggle( self.devices[name].channel )

  def getDeviceState(self, name):
    if name in self.devices:
      return self.getState( self.devices[name].channel )
    else:
      return None
