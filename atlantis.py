#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

from globalconfig import GlobalConfig

import relay
import rotary
import display
import menu
import sensors
import leds
import streaming
from xmlrpc_server import XMLRPC_Server


import time

leds = leds.RGBLEDStrip(GlobalConfig.leds_r, GlobalConfig.leds_g, GlobalConfig.leds_b)
leds.off()

sensors = sensors.Sensors()

dpy = display.Display()
dpy.printMessage("Initializing...", 0)

relays = relay.RelayModule( GlobalConfig.relay_pins )
dpy.printMessage("Relay module with " + str(relays.size()) + " relay(s)")
for dev in GlobalConfig.relay_devices:
  relays.registerDevice(dev[0], dev[1])

stream = streaming.Stream()

xmlrpc_server = XMLRPC_Server(relays, stream, sensors)

rot = rotary.RotaryEncoder()

main_menu = menu.Menu(rot, dpy, relays, stream)


def populateDisplay():  
    dpy.printMessage(sensors.getDisplay16x2Line1(),0)
    dpy.printMessage(sensors.getDisplay16x2Line2(),1)


try:

    while True:
        time.sleep(0.1)
        if ( not main_menu.iter() ):
            populateDisplay()

except KeyboardInterrupt:
    pass

finally:
    print("Bye, bye!")
    dpy.setBacklight(0)
    xmlrpc_server.stop()
    xmlrpc_server.join()
    sensors.stop()
    # GPIO cleanup (just in case...)
    GPIO.cleanup()
