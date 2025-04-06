#!/usr/bin/python3
#

import threading
import datetime
import time
from globalconfig import GlobalConfig
import relay

class TimedEvent:
  def __init__(self):
    pass
    # TO-DO: define timed events


class Chronos(threading.Thread):

  # TO-DO: display -- manage priority messages, duration, message queues...
  def __init__(self, relays):
    threading.Thread.__init__(self)
    self.name = "Chronos"
    self.done = False
    self.relays = relays
    # First event - TEMPORARY HACK!
    self.next_event = datetime.datetime.now()
    if self.next_event.hour < 6: # before UTC 6:00
      self.next_event = self.next_event.replace(hour=6, minute=0, second=0, microsecond=0)
    elif self.next_event.hour < 21: # after UTC 6:00 and before UTC 21:00
      self.next_event = self.next_event.replace(hour=21, minute=0, second=0, microsecond=0)
    else: # after UTC 21:00
      self.next_event += datetime.timedelta(days=1)
      self.next_event = self.next_event.replace(hour=6, minute=0, second=0, microsecond=0)
    self.start()

  def __del__(self):
    pass
    
  def run(self):
    while not self.done:
      now = datetime.datetime.now()
      delta = self.next_event - now
#      print("NOW: ", now)
#      print("EVENT: ", self.next_event)
#      print("DELTA: ", delta)
      if delta.total_seconds() < 0. :
        # quick hack to light programming on holidays
        # identify the event
        if self.next_event.hour == 6: # UTC 6:00 --> localtime 8:00
#          print("EVENT! ", self.next_event, " - FLUORESCENT ON!!!")
          self.relays.turnOnDevice("fluorescent")
          self.next_event = self.next_event.replace(hour=21)
        else: #elif self.next_event.hour == 21: # UTC 21:00 --> localtime 23:00
#          print("EVENT! ", self.next_event, " - FLUORESCENT OFF!!!")
          self.relays.turnOffDevice("fluorescent")
          self.next_event += datetime.timedelta(days=1)
          self.next_event = self.next_event.replace(hour=6)
      time.sleep(1)

  def stop(self):
    self.done = True


if __name__ == '__main__':	# Testing code

  relays = relay.RelayModule( GlobalConfig.relay_pins )
  for dev in GlobalConfig.relay_devices:
    relays.registerDevice(dev[0], dev[1])
  chronos = Chronos(relays)
  
  try:
    while True:
      print("Chronos is working...")
      time.sleep(1)
    
  except:
    chronos.stop()
    chronos.join()
    
  finally:
    pass
  