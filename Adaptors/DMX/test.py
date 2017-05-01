"""
1 pump
4 pump
5 
6
7
9


"""

import time

import threading

from main import init as dmx_init

dmx = dmx_init(universe=0,frame_size=40)


r = 255

while True:
    for val in range(r):
        print "value=", val
        for ch in range (40):
            if ch == 8:
                dmx.set(ch, int(val/2.0))
            else:
                dmx.set(ch, val)
        #dmx.set(8, 0)
        time.sleep(0.1)
    for val in range(r):
        print "value=", val
        for ch in range (40):
            if ch == 8:
                dmx.set(ch, int((r-val)/2.0))
            else:
                dmx.set(ch, r-val)
        #dmx.set(8, 0)
        time.sleep(0.1)