    
import time

import threading

from main import init as dmx_init

dmx = dmx_init(universe=0,frame_size=40)

while True:
    for ch in range (40):
        dmx.set(ch, 0)
        time.sleep(0.5)
