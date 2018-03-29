#!/usr/bin/python3
#

import RPi.GPIO as GPIO

class RelayModule:

    def __init__(self, relay_pins):
        self.relay_pins = relay_pins
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
        return GPIO.input(self.relay_pins[ch])
