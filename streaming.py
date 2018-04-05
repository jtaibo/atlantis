#!/usr/bin/python3
#

import threading
import time
import subprocess
import shlex
import os


class StreamingThread(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
#    os.system("sudo modprobe bcm2835-v4l2")
    self.start()

  def run(self):
    try:
      cmd_p1 = "raspivid -o - -t 0 -hf -w 960 -h 540 -fps 25"
      cmd_p2 = "cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264"
      self.p1 = subprocess.Popen( shlex.split(cmd_p1), stdout=subprocess.PIPE)
      self.p2 = subprocess.Popen( shlex.split(cmd_p2), stdin=self.p1.stdout, stdout=subprocess.PIPE)
#      print( self.p2.communicate() )
    except:
      print("StreamingThread died!")

  def stop(self):
    if self.p1:
      self.p1.terminate()
      self.p2.terminate()
      try:
        self.p1.wait(timeout=2)
      except TimeoutExpired:
        self.p1.kill()
      try:
        self.p2.wait(timeout=2)
      except TimeoutExpired:
        self.p2.kill()


class Stream:

  def __init__(self):
    self.running = False

  def start(self):
    if not self.running:
      try:
        self.running = True
        self.st = StreamingThread()
      except CalledProcessError:
        self.running = False

  def stop(self):
    if self.running:
      self.st.stop()
      self.running = False

  def isOn(self):
    return self.running


if __name__ == '__main__':     # Testing code

  print( "Testing streaming service" )
  stream = Stream()
  print( "Streaming status is ", stream.isOn() )
  print( "Starting streaming..." )
  stream.start()
  print( "Streaming status is ", stream.isOn() )
  time.sleep(20)
  print( "Terminating streaming..." )
  stream.stop()
  print( "Streaming status is ", stream.isOn() )
