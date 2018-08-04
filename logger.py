#!/usr/bin/python3
#

from globalconfig import GlobalConfig
import sensors
import threading
import time
import arduinocomm

class Logger(threading.Thread):

  def __init__(self, sensors):
    threading.Thread.__init__(self)
    self.sensors = sensors
    self.log_sensor_check_time = 1  # check every second
    self.log_sensor_cycle_time = 60 # write every minute
    self.log_filename = "/opt/atlantis/log/sensors.log"
    self.log_file = open(self.log_filename, "a")
    self.done = False
    self.last_write_time = -1
    self.start()

  def __del__(self):
    pass

  def printLogLine(self):
    timestamp = time.time()
    line = str(timestamp) \
      + " " + str(self.sensors.getAirTemperature()) \
      + " " + str(self.sensors.getAirHumidity()) \
      + " " + str(self.sensors.getWaterTemperature()) \
      + " " + str(self.sensors.getWaterPH()) + "\n"
    self.log_file.write(line)
    self.log_file.flush()

  def run(self):
    while not self.done:
      if time.time() - self.last_write_time > self.log_sensor_cycle_time:
        self.last_write_time = time.time()
        # Log sensor data
        self.printLogLine()
      time.sleep(self.log_sensor_check_time)

  def stop(self):
    self.done = True
    self.log_file.close()


if __name__ == '__main__':     # Testing code

  arduino_comm = arduinocomm.ArduinoComm()
  the_sensors = sensors.Sensors(arduino_comm)
  logger = Logger(the_sensors)

  try:
    while True:
      print("Still alive")
      time.sleep(1)

  except KeyboardInterrupt:
    the_sensors.stop()
    arduino_comm.stop()
    logger.stop()
