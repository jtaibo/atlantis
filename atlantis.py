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
import arduinocomm
from xmlrpc_server import XMLRPC_Server
import signal
import sys
import time
import logger
#import chronos

print("Starting atlantis service...")
dpy = display.Display()
dpy.printMessage("Initializing...", 0)

dpy.printMessage("Arduino comm", 1)
arduino_comm = arduinocomm.ArduinoComm()

dpy.printMessage("LED strip", 1)
leds = leds.RGBLEDStrip(GlobalConfig.leds_r, GlobalConfig.leds_g, GlobalConfig.leds_b)
leds.configPWM()

dpy.printMessage("Sensors", 1)
sensors = sensors.Sensors(arduino_comm)

dpy.printMessage("Relays", 1)
relays = relay.RelayModule( GlobalConfig.relay_pins )
for dev in GlobalConfig.relay_devices:
  relays.registerDevice(dev[0], dev[1])

dpy.printMessage("Streaming", 1)
stream = streaming.Stream()

# Wait some seconds, to wait for the network to be completely configured before trying to start the server
#time.sleep(10)
xmlrpc_server = XMLRPC_Server(relays, stream, sensors, leds)

dpy.printMessage("Rotary encoder", 1)
rot = rotary.RotaryEncoder()

dpy.printMessage("Menu", 1)
main_menu = menu.Menu(rot, dpy, relays, stream)

dpy.printMessage("Logger")
log_mgr = logger.Logger(sensors)

#dpy.printMessage("Chronos")
#cron = chronos.Chronos(relays)


def populateDisplay():  
    dpy.printMessage(sensors.getDisplay16x2Line1(),0)
    dpy.printMessage(sensors.getDisplay16x2Line2(),1)

def gracefulExit():
    print("Bye, bye!")
    dpy.printMessage(" ---SHUTDOWN--- ", 0)
    dpy.printMessage("                ", 1)
    dpy.setBacklight(0)
    xmlrpc_server.stop()
    xmlrpc_server.join()
    log_mgr.stop()
    sensors.stop()
    arduino_comm.stop()
#    cron.stop()
    # GPIO cleanup (just in case...)
    GPIO.cleanup()

def sigterm_handler(signal, frame):
    print("SIGTERM signal received")
    sys.exit(0) # Will execute the finally: code (hopefully)

signal.signal(signal.SIGTERM, sigterm_handler)


try:

    print("Service initialized")

    while True:
        time.sleep(0.1)
        if ( not main_menu.iter() ):
            populateDisplay()

except KeyboardInterrupt:
    pass

finally:
    gracefulExit()
