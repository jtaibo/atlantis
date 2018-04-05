#!/usr/bin/python3
#

from globalconfig import GlobalConfig
import dht11mt
import ds18b20
import time


class Sensors:

  def __init__(self):
    self.dht11 = dht11mt.DHT11_MT( GlobalConfig.DHT11_data_pin )
    self.water_temp = ds18b20.DS18b20( GlobalConfig.water_temp_sensor_id )

  def stop(self):
    self.water_temp.stop()
    self.dht11.stop()
    self.water_temp.join()
    self.dht11.join()

  def getAirTemperature(self):
    return self.dht11.getTemperature()
    
  def getAirHumidity(self):
    return self.dht11.getHumidity()

  def getWaterTemperature(self):
    return self.water_temp.getTemp()

  def getWaterPH(self):
    # TO-DO implement me!
    return 7.1

  # TO-DO:
  #  - Light sensor
  #  - ...

  def getSensorsJSON(self):
    return { 
        "air_temperature" : self.getAirTemperature(),
        "air_humidity" : self.getAirHumidity(),
        "water_temperature" : self.getWaterTemperature(),
        "water_ph" : self.getWaterPH()
      }

  def getDisplay16x2Line1(self):
    return "T " + "{:2.2f}".format(self.getAirTemperature()) + " C Hu " + str(self.getAirHumidity()) + "%"

  def getDisplay16x2Line2(self):
    return "T " + "{:2.2f}".format(self.getWaterTemperature()) + " C pH " + str(self.getWaterPH())


if __name__ == '__main__':     # Testing code

  print( "Testing sensor manager module" )
  sensors = Sensors()
  try:
    while [ True ]:
      print( sensors.getSensorsJSON() )
      time.sleep(1)
  except KeyboardInterrupt:
    pass
  sensors.stop()
