#!/usr/bin/python
#

import rotary
import relay
import display
from globalconfig import GlobalConfig

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
  def __init__(self, name, relays, idx):
    MenuItem.__init__(self, name)
    self.relays = relays
    self.idx = idx

  def getDisplayStringL1(self):
    # Inverted because relays are enabled when GPIO is low
    if ( self.relays.getState(self.idx) ):
      return "OFF"
    else:
      return "ON"

  def click(self):
    self.relays.toggle(self.idx)


class BacklightMI(MenuItem):
  def __init__(self, name):
    MenuItem.__init__(self, name)
    
  def getDisplayStringL1(self):
    if GlobalConfig.keepDisplayBacklight:
      return "ON"
    else:
      return "OFF"
    
  def click(self):
    GlobalConfig.keepDisplayBacklight = not GlobalConfig.keepDisplayBacklight


class Menu:

    def __init__(self, rot, dpy, relays):

        self.menuItems = [
                            BacklightMI("Backlight"),
                            RelayMI("Filtro", relays, 0),
                            RelayMI("Bomba", relays, 1),
                            RelayMI("Fluorescente", relays, 2)
                            ]
        self.rot = rot
        self.dpy = dpy
        self.relays = relays
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
