#!/usr/bin/python3
#

import RPi.GPIO as GPIO
import dht11
import time
import threading


class DHT11_MT(threading.Thread):
  
  def __init__(self, sensor_pin, cycle=1):
    threading.Thread.__init__(self)
    GPIO.setmode(GPIO.BCM)
    self.dht11_sensor = dht11.DHT11(pin = sensor_pin)
    self.cycle_time = cycle
    self.temperature = -1
    self.humidity = -1
    self.done = False
    self.start()

  def __del__(self):
    pass

  def run(self):
    while not self.done:
      result = self.dht11_sensor.read()
      if result.is_valid():
        self.temperature = result.temperature
        self.humidity = result.humidity
      time.sleep(self.cycle_time)

  def getTemperature(self):
    return self.temperature

  def getHumidity(self):
    return self.humidity

  def stop(self):
    self.done = True


if __name__ == '__main__':     # Testing code

  dht11_sensor = DHT11_MT(21)

  try:
    while True:
      print(dht11_sensor.getTemperature(), dht11_sensor.getHumidity())	
      time.sleep(0.1)

  except:
    dht11_sensor.stop()
    dht11_sensor.join()
