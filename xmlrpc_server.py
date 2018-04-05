#!/usr/bin/python3
#

from xmlrpc.server import DocXMLRPCServer
from xmlrpc.server import DocXMLRPCRequestHandler

import threading
import time

from globalconfig import GlobalConfig
import relay
import sensors


class XMLRPC_Server(threading.Thread):

  def __init__(self, relays, stream, sensors):
    self.relays = relays
    self.stream = stream
    self.sensors = sensors
    threading.Thread.__init__(self)
    self.start()

  def stop(self):
    self.server.shutdown()
    self.server.server_close()

  def run(self):
  
    class RequestHandler(DocXMLRPCRequestHandler):

      rpc_paths = ('/AtlantisRPC',)

      def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

      # Add these headers to all responses
      def end_headers(self):
        self.send_header("Access-Control-Allow-Headers", 
                         "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        DocXMLRPCRequestHandler.end_headers(self)

    self.server=DocXMLRPCServer((GlobalConfig.xmlrpc_host, GlobalConfig.xmlrpc_port),
                        requestHandler=RequestHandler)
    self.server.set_server_title("Atlantis RPCXML server")
    self.server.set_server_name("Atlantis RPCXML server")
    self.server.set_server_documentation("Atlantis RPCXML server documentation")
    self.server.register_introspection_functions()
    self.server.register_function(self.get_status)
    self.server.register_function(self.set_device)
    self.server.register_function(self.turn_on_device)
    self.server.register_function(self.turn_off_device)
    self.server.register_function(self.toggle_device)
    self.server.register_function(self.turn_on_stream)
    self.server.register_function(self.turn_off_stream)
    self.server.register_function(self.toggle_stream)
    self.server.serve_forever()

  # XMLRPC methods

  def get_status(self):
    status = { "sensors": self.sensors.getSensorsJSON(),
               "leds": [
                   {
                    "mode":"static",
                    "r": 1.0,
                    "g": 1.0,
                    "b": 1.0
                   }
                 ],
               "relays": {},
               "streaming": self.stream.isOn()
             }
    # Insert relay status
    for r in self.relays.devices:
      status["relays"][r] = self.relays.getDeviceState(r)
    return status

  def set_device(self, id, value):
    if value:
      self.relays.turnOnDevice(id)
    else:
      self.relays.turnOffDevice(id)
    return self.get_status()

  def turn_on_device(self, id):
    self.relays.turnOnDevice(id)
    return self.get_status()

  def turn_off_device(self, id):
    self.relays.turnOffDevice(id)
    return self.get_status()

  def toggle_device(self, id):
    self.relays.toggleDevice(id)
    return self.get_status()

  def turn_on_stream(self):
    self.stream.start()

  def turn_off_stream(self):
    self.stream.stop()

  def toggle_stream(self):
    if self.stream.isOn():
      self.stream.stop()
    else:
      self.stream.start()


if __name__ == '__main__':     # Testing code

  try:
    server = XMLRPC_Server()
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("Hasta logo!")

  server.stop()
  print("This is the end!")
