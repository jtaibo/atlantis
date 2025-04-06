#!/usr/bin/python3
#

import serial
import time
import threading
from globalconfig import GlobalConfig


class ArduinoComm(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.done = False
    self.pH = -1
    self.AC_current = -1
#    self.ser = serial.Serial(GlobalConfig.arduino_serial_port, GlobalConfig.arduino_baud_rate)
    self.name = "ArduinoComm"
    self.start()

  def __del__(self):
    pass

  def run(self):
    while not self.done:
#      read_serial = self.ser.readline()
#      line = read_serial.decode("ascii")
#      key, val = line.split(" ")
      key = "pH"
      val = "7"
#      print( "key:", key, " val:", val)
      if key == "pH":
        self.pH = float(val)
      elif key == "AC":
        self.AC_current = float(val)
      time.sleep(0.1)
    
  def uploadProgram(self):
    pass

  def getPH(self):
    return self.pH
  
  def getACCurrent(self):
    return self.AC_current

  def stop(self):
    self.done = True

if __name__ == '__main__':     # Testing code

  arduino_comm = ArduinoComm()

  try:
    while True:
      print( "pH = ", arduino_comm.getPH() )
      print( "AC = ", arduino_comm.getACCurrent(), " A" )
      time.sleep(1)

  except:
    arduino_comm.stop()
    arduino_comm.join()

  finally:
    pass
