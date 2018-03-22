import spidev
import time
import RPi.GPIO as GPIO

class AMT203():
  def __init__(self, bus=0, deviceId=0):
    self.deviceId = deviceId
    self.bus = bus
    # self.pin = pin
    GPIO.setmode(GPIO.BCM)
    # GPIO.setup(self.pin, GPIO.OUT)
    # GPIO.output(self.pin, GPIO.HIGH)
    try:
      print "bus: %s | pin: %s" % (self.bus, self.deviceId)
      self.spi = spidev.SpiDev()
      self.spi.open(self.bus,self.deviceId)
      self.open = True
      print "SPI connected. Device id: ", self.deviceId
    except:
      self.open = False
      print "Could not connect to SPI device"

  def clean_buffer(self):
    first_result = self.spi.xfer([0x00],0,20)
    while first_result[0] != 165:
      # print first_result[0]
      first_result = self.spi.xfer([0x00],0,20)
    # print "Buffer empty"

  def get_position(self):
    first_result = self.spi.xfer([0x10],0,20)
    while first_result[0] != 16:
      first_result = self.spi.xfer([0x00],0,20)
    msb_result = self.spi.xfer([0x00],0,20)
    lsb_result = self.spi.xfer([0x00],0,20)
    # print "MSB: %s | LSB: %s " % (msb_result, lsb_result)
    # msb_bin = bin(msb_result[0]<<8)[2:]
    # lsb_bin = bin(lsb_result[0])[2:]
    final_result = (msb_result[0]<<8 | lsb_result[0])
    # print "Final: ", final_result
    self.clean_buffer()
    return final_result

  def set_zero(self):
    self.clean_buffer()
    first_result = self.spi.xfer([0x70],0,20)
    while first_result[0] != 128:
      # print first_result[0]
      first_result = self.spi.xfer([0x00],0,20)
    print "Zero set was successful and the new position offset is stored in EEPROM"
    self.clean_buffer()
    # GPIO.output(self.pin, GPIO.LOW)
    time.sleep(0.1)
    # GPIO.output(self.pin, GPIO.HIGH)

  def get_resolution(self):
    return 4096
