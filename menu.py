#!/usr/bin/python3
#

import rotary
import relay
import display
from globalconfig import GlobalConfig
import os


# States
ST_OFF = 0
ST_ON = 1

MENU_TIMEOUT = 5
BACKLIGHT_TIMEOUT = 15


class MenuItem:
  def __init__(self, name):
    self.name = name
    
  def getDisplayStringL0(self):
    return self.name
    
  def getDisplayStringL1(self):
    return ""
    
  def click(self):
    pass


class RelayMI(MenuItem):
  def __init__(self, name, relays, id):
    MenuItem.__init__(self, name)
    self.relays = relays
    self.id = id

  def getDisplayStringL1(self):
    if ( self.relays.getDeviceState(self.id) ):
      return "ON"
    else:
      return "OFF"

  def click(self):
    self.relays.toggleDevice(self.id)


class BacklightMI(MenuItem):
  def __init__(self, name):
    MenuItem.__init__(self, name)
    
  def getDisplayStringL1(self):
    if GlobalConfig.keepDisplayBacklight:
      return "ON"
    else:
      return "Auto-OFF"
    
  def click(self):
    GlobalConfig.keepDisplayBacklight = not GlobalConfig.keepDisplayBacklight


class StreamingMI(MenuItem):
  def __init__(self, name, stream):
    MenuItem.__init__(self, name)
    self.stream = stream

  def getDisplayStringL1(self):
    if self.stream.isOn():
      return "enabled"
    else:
      return "disabled"

  def click(self):
    if self.stream.isOn():
      self.stream.stop()
    else:
      self.stream.start()

class CommandMI(MenuItem):
  def __init__(self, name, cmd):
    MenuItem.__init__(self, name)
    self.cmd = cmd

  def getDisplayStringL1(self):
    return ""

  def click(self):
    os.system(self.cmd)

class ExitMI(MenuItem):
  def __init__(self, name):
    MenuItem.__init__(self, name)

  def getDisplayStringL1(self):
    return ""

  def click(self):
    exit(0)
    

class Menu:

    def __init__(self, rot, dpy, relays, stream):

        self.menuItems = [
                            BacklightMI("Dpy Backlight"),
                            RelayMI(    "Filter", relays, "filter"),
                            RelayMI(    "Air pump", relays, "airpump"),
                            RelayMI(    "Fluorescent", relays, "fluorescent"),
                            RelayMI(    "Heater", relays, "heater"),
                            StreamingMI("Video Streaming", stream),
                            CommandMI(  "Shutdown", "sudo poweroff"),
                            ExitMI(     "Exit")
                            ]
        self.rot = rot
        self.dpy = dpy
        self.relays = relays
        self.stream = stream
        self.previous_option = self.getCurrentOption()
        self.state = ST_OFF
        self.backlight = False

    def getCurrentOption(self):
        return self.rot.getCounter() % len(self.menuItems)

    def iter(self):
        if ( self.state == ST_OFF ):
            if ( self.rot.getLastIterationDelta() < MENU_TIMEOUT ):                
                self.turnOn()
        elif ( self.state == ST_ON ):
            if ( self.rot.getLastIterationDelta() > MENU_TIMEOUT ):
                self.turnOff()
            else:
                if ( self.rot.getNewClick() ):
                  self.menuItems[self.getCurrentOption()].click()
                  self.updateOption()
                if ( self.previous_option != self.getCurrentOption() ):
                  self.updateOption()
        if ( not GlobalConfig.keepDisplayBacklight and self.backlight and self.rot.getLastIterationDelta() > BACKLIGHT_TIMEOUT ):
            self.dpy.setBacklight(0)
            self.backlight = False
        return ( self.state == ST_ON )

    def updateOption(self):
        self.dpy.printMessage( self.menuItems[self.getCurrentOption()].getDisplayStringL0(), 0 )
        self.dpy.printMessage( self.menuItems[self.getCurrentOption()].getDisplayStringL1(), 1 )
        self.previous_option = self.getCurrentOption()

    def turnOn(self):
        self.state = ST_ON
        self.dpy.clear()
        self.dpy.setBacklight(1)
        self.backlight = True
        self.updateOption()
        self.rot.getNewClick()	# Discard any clicks until display is on

    def turnOff(self):
        self.state = ST_OFF
        self.dpy.clear()


if __name__ == '__main__':     # Testing code
    pass
