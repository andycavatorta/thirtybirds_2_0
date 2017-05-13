import spidev
import time
import RPi.GPIO as GPIO

class TLC1543IN():
    def __init__(self, bus=0, deviceId=0):
        self.deviceId = deviceId
        self.bus = bus
        GPIO.setmode(GPIO.BCM)
        
    def read(self, channel):
        return 0