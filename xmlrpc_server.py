#!/usr/bin/python3
#

from xmlrpc.server import DocXMLRPCServer
from xmlrpc.server import DocXMLRPCRequestHandler

import threading
import time

from globalconfig import GlobalConfig
import relay


class XMLRPC_Server(threading.Thread):

  def __init__(self, relays):
    self.relays = relays
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
    self.server.register_function(self.toggle_relay, "toggle_relay")
    self.server.serve_forever()

  # XMLRPC methods

  def get_status(self):
    status = { "sensors": {
                  "airtemp": 20.0,
                  "humidity": 41,
                  "watertemp": 20.59,
                  "pH": 7.1
                 },
               "leds": [
                   {
                    "mode":"static",
                    "r": 1.0,
                    "g": 1.0,
                    "b": 1.0
                   }
                 ],
               "relays": [
               ]
             }
    # Insert relay status
    for i in range(self.relays.size()):
      status["relays"].append(self.relays.getState(i))
    return status

  def set_filter(self):
    pass
  def get_filter(self):
    pass
  
  def set_fluorescent(self):
    pass
  def get_fluorescent(self):
    pass

  def set_airpump(self):
    pass
  def get_airpump(self):
    pass
  
  def set_heater(self):
    pass
  def get_heater(self):
    pass

  def toggle_relay(self, channel):
    self.relays.toggle(channel)
    output = "Relay " + channel + " status: " + self.relays.getState(channel)
    return output


if __name__ == '__main__':     # Testing code

  try:
    server = XMLRPC_Server()
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print("Hasta logo!")

  server.stop()
  print("This is the end!")
