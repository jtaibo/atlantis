#!/usr/bin/python
#

import os
import glob
import time
import threading


class DS18b20(threading.Thread):
  
  def __init__(self, sensor_id='', cycle=1):
    threading.Thread.__init__(self)
    self.sensor_id = sensor_id
    self.cycle_time = cycle
    self.temp_c = -1
    self.done = False
    # No need to load these modules, they are automatically loaded on startup
    # This should be done as root, anyway...
    #os.system('modprobe w1-gpio')
    #os.system('modprobe w1-therm')
    # Don't need to set the GPIO pin as long as it is de default one (pin 4)
    #os.system('dtoverlay w1-gpio gpiopin=4 pullup=0')

    self.base_dir = '/sys/bus/w1/devices/'
    if not self.sensor_id:
      self.device_folder = glob.glob(self.base_dir + '28*')[0]
    else:
      self.device_folder = self.base_dir + self.sensor_id
    self.device_file = self.device_folder + '/w1_slave'
    self.start()

  def __del__(self):
    pass

  def run(self):
    while not self.done:
      self.read_temp()
      time.sleep(self.cycle_time)

  def read_temp_raw(self):
    f = open(self.device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

  def read_temp(self):
    lines = self.read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = self.read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        self.temp_c = float(temp_string) / 1000.0
        return self.temp_c
        
  def getTemp(self):
    return self.temp_c

  def stop(self):
    self.done = True


if __name__ == '__main__':     # Testing code

  temp_sensor = DS18b20()

  try:
    while True:
      print(temp_sensor.getTemp())	
      time.sleep(0.1)
  except:
    temp_sensor.stop()
    temp_sensor.join()
