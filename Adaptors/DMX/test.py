"""
1 pump
4 pump
5 
6
7
9


"""

#/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AL0409S4-if00-port0
#   `./special_baud_rate.py <>/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AL0409S4-if00-port0 250000

import time

import threading

from main import init as dmx_init
                              
dmx = dmx_init(devicePattern="usb-ENTTEC_DMX_USB_PRO_EN237782-if00-port0",frame_size=40)

r = 255

while True:
    for ch in range(10):

        for val in range(r):
            print "channel={} value={}".format(ch,val)
            dmx.set(ch, val)
            time.sleep(0.01)
        for val in range(r):
            print "channel={} value={}".format(ch,val)
            dmx.set(ch, r-val)
            time.sleep(0.01)
