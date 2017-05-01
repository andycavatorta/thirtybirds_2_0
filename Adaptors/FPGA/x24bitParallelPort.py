"""
"""
import os
import time

PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi

if PI_NATIVE:
    import RPi.GPIO as GPIO
else:
    import RPi_stub.GPIO as GPIO

INTRA_WORD_TIMING = 0.01 # SECONDS
#TX_PINS = [2,3,14,4,15,18,17,27,23,24,10,9,25,11,8,7,5,6,12,13,16,19,20,26] # pin 22 is wired but not used
#TX_PINS = [14,4,15,18,17,27,23,24,10,9,25,11,8,7,5,6,12,13,16,19,20,26,21] # pin 22 is wired but not used
TX_PINS = [26,20,19,16,13,6,12,5,7,11,8,9,25,10,24,22,23,27,17,18,15,4,14] # pin 22 is wired but not used

DATA_READY_PIN = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_READY_PIN,GPIO.OUT)
for pin in TX_PINS:
    GPIO.setup(pin,GPIO.OUT)

def send(word_bin_a): # word_ba must be 23 bit-characters long
    #print "x24ParallalPort.send word ", word_bin_a
    
    GPIO.output(DATA_READY_PIN  ,0)
    word_bin_a += [0] * (len(TX_PINS) - len(word_bin_a)) # pad word_bin_a with zeroes
    for i in range(len(TX_PINS)):
        #print "x24ParallalPort.send ", i, TX_PINS[i], int(word_bin_a[i])
        GPIO.output(TX_PINS[i],int(word_bin_a[i]))
    #time.sleep(INTRA_WORD_TIMING) # this is a cheap-ass solution.  But it's simple and efficient.  Could replace with threads and queues in the future.
    GPIO.output(DATA_READY_PIN,1)
    
    GPIO.output(DATA_READY_PIN  ,0)
    word_bin_a += [0] * (len(TX_PINS) - len(word_bin_a)) # pad word_bin_a with zeroes
    for i in range(len(TX_PINS)):
        #print "x24ParallalPort.send ", i, TX_PINS[i], int(word_bin_a[i])
        GPIO.output(TX_PINS[i],int(word_bin_a[i]))
    #time.sleep(INTRA_WORD_TIMING) # this is a cheap-ass solution.  But it's simple and efficient.  Could replace with threads and queues in the future.
    GPIO.output(DATA_READY_PIN,1)
    #print "x24ParallalPort.send word sent", word_bin_a