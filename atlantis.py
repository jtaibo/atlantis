#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

from globalconfig import GlobalConfig

import relay
import rotary
import display
import menu
import dht11mt
import ds18b20
import leds
from xmlrpc_server import XMLRPC_Server


import time

leds = leds.RGBLEDStrip(GlobalConfig.leds_r, GlobalConfig.leds_g, GlobalConfig.leds_b)
leds.off()

dht11 = dht11mt.DHT11_MT( GlobalConfig.DHT11_data_pin )
water_temp = ds18b20.DS18b20( GlobalConfig.water_temp_sensor_id )

dpy = display.Display()
dpy.printMessage("Initializing...", 0)

relays = relay.RelayModule( GlobalConfig.relay_pins )
dpy.printMessage("Relay module with " + str(relays.size()) + " relay(s)")
for dev in GlobalConfig.relay_devices:
  relays.registerDevice(dev[0], dev[1])

xmlrpc_server = XMLRPC_Server(relays)

rot = rotary.RotaryEncoder()

def testRelays():
    for i in range(8):
        dpy.printMessage("Testing relay #" + str(i), 0)
        relays.on(i)
        time.sleep(0.3)
        relays.off(i)

    time.sleep(1)

    for i in range(4):
        for p in range(8):
            relays.toggle(p)
            time.sleep(0.2)
    dpy.printMessage("OK!", 0)

main_menu = menu.Menu(rot, dpy, relays)

def populateDisplay():
    # 1234567890123456
    # T 21ºC  H 40%
    # T 10ºC  pH 7.1

    air_temperature = dht11.getTemperature()
    air_humidity = dht11.getHumidity()

    water_temperature = water_temp.getTemp()
    water_pH = 7.1	# Temporary placeholder

    line1 = "T " + "{:2.2f}".format(air_temperature) + " C Hu " + str(air_humidity) + "%"
    line2 = "T " + "{:2.2f}".format(water_temperature) + " C pH " + str(water_pH)
    dpy.printMessage(line1,0)
    dpy.printMessage(line2,1)

#testRelays()

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
    water_temp.stop()
    dht11.stop()
    xmlrpc_server.stop()
    water_temp.join()
    dht11.join()
    xmlrpc_server.join()
    # GPIO cleanup (just in case...)
    GPIO.cleanup()
