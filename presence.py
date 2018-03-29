#!/usr/bin/python3
#

import threading
import time
from globalconfig import GlobalConfig

import bluetooth


class Presence(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    # to-do: registered users should go in global config
    self.registered_users = []
    self.done = False
    self.cycle_time = 1
    self.start()

  def run(self):
    while not self.done:
      # to-do
      time.sleep(self.cycle_time)

  def stop(self):
    self.done = True

  def getPresenceStatusReport(self):
    return "NOT IMPLEMENTED... YET"


if __name__ == '__main__':     # Testing code

  pre = Presence()

  try:

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
      print("  %s - %s" % (addr, name))

    result = bluetooth.lookup_name('A8:96:75:8B:A3:9A', timeout=5)
    if (result != None):
        print "Javi: in"
    else:
        print "Javi: out"



    while True:
      print(pre.getPresenceStatusReport())
      time.sleep(1)

  except:
    pre.stop()
    pre.join()
