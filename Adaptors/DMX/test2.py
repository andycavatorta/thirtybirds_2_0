
import time

import threading

from main import init as dmx_init

dmx = dmx_init(universe=0,frame_size=40)

while True:
    for ch in range (10):
        for val in range(180):
            print "channel =", ch, "value=", val
            dmx.set(ch, val)
            time.sleep(0.05)
        for val in range(180):
            v = 180-val
            print "channel =", ch, "value=", v
            dmx.set(ch, v)
            time.sleep(0.05)