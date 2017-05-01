import os
import serial
import threading
import time

SOM_VALUE = 0x7E
EOM_VALUE = 0xE7
OUTPUT_ONLY_SEND_DMX_LABEL  = 6

class DMX(threading.Thread):
  def __init__(self, usbId, frame_size, universe, refreshPeriod):
    threading.Thread.__init__(self)
    self.refreshPeriod = refreshPeriod
    self.usbId = usbId
    self.universe = universe
    self.frame_size = frame_size
    self.frame = [0]*frame_size
    self.port = False
    self.open()

  def open(self):
    self.port = serial.Serial(self.usbId, 115200, timeout=1)

  def close(self):
    if self.port:
      self.port.close()

  def set(self, channel, value):
    self.frame[channel-1] = value

  def get(self, channel):
    return self.frame[channel]

  def make_frame(self):
    frame = ""
    frame += chr(SOM_VALUE)
    frame += chr(OUTPUT_ONLY_SEND_DMX_LABEL)
    frame += chr(self.frame_size & 0xFF)
    frame += chr((self.frame_size >> 8) & 0xFF)
    frame += chr(self.universe)
    for j in range(self.frame_size):
      #print ">>>>>>>>>>>>>>>", self.frame[j]
      frame += chr(self.frame[j])
    frame += chr(EOM_VALUE)
    return frame

  def send(self, frame):
    if self.port:
      #print repr(frame)
      try:
        self.port.write(frame)
      except Exception as e:
        print "SerialException", e
        self.open()

  def run(self):
    while True:
      self.send(self.make_frame())
      time.sleep(self.refreshPeriod)

def get_dmx_interface(searchString):
  for file in os.listdir("/dev/serial/by-id"):
    if searchString in file:
      return file
  return ""


def init(devicePattern="DMX", frame_size=512, universe=0, refreshPeriod=0.025):
  dmxDeviceName = get_dmx_interface(devicePattern)
  
  if dmxDeviceName=="":
    print "DMX interface not found"
    return False

  usbId = "/dev/serial/by-id/%s" % (dmxDeviceName)
  print usbId
  dmx = DMX(usbId, frame_size, universe, refreshPeriod)
  dmx.start()
  return dmx

