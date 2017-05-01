import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class SPI_ADC():
    def __init__(self, clk=18, cs=25, miso=23, mosi=24):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        self.mcp = Adafruit_MCP3008.MCP3008(clk, cs, miso, mosi)

    def read(self, channel):
        return self.mcp.read_adc(channel)



def init():
    return SPI_ADC()