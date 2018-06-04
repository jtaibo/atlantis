#!/usr/bin/python3
#

import RPi

class GlobalConfig:

  keepDisplayBacklight = False

  # Pin configuration (BCM)
#  GPIO_mode = RPi.GPIO.BCM

  # Display - interface I2C
  # SDA - pin 2
  # SCL - pin 3

#  DHT11_data_pin = 21
  DHT11_data_pin = 12

  pir_pin = 18

  # Water temperature sensor: 1-Wire interface - pin 4
  water_temp_sensor_id = '28-041701b47aff'

#  relay_pins = [14, 15, 18, 23, 24, 25, 8, 7]
  relay_pins = [17, 27, 22, 5, 6, 13, 19, 26]

  relay_devices = [
                    ("filter", 0),
                    ("airpump", 1),
                    ("fluorescent", 2),
                    ("heater", 3)
                  ]

  # Rotary encoder
#  rotary_clk_pin = 22
#  rotary_dt_pin = 27
#  rotary_sw_pin = 17
  rotary_clk_pin = 21
  rotary_dt_pin = 20
  rotary_sw_pin = 16

  # LED strips
  leds_r = 24
  leds_g = 23
  leds_b = 25

  # Known BT MACs
  bt_macs = [
              {"Javi", "A8:96:75:8B:A3:9A"}
            ]

  # XMLRPC server
  xmlrpc_host = "atlantis"
#  xmlrpc_host = "localhost"
  xmlrpc_port = 8000

  arduino_serial_port = "/dev/ttyUSB0"
  arduino_baud_rate = 9600
