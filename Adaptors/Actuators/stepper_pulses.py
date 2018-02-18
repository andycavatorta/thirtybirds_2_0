import Queue
import RPi.GPIO as GPIO
import threading
import time

class Channel(threading.Thread):
    def __init__(self, pulse_pin, dir_pin, base_pulse_period = 0.001, steps_finished_callback = False, backwards_orientation = False):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.pulse_pin = pulse_pin
        self.dir_pin = dir_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)
        self.backwards_orientation = backwards_orientation
        self.steps_finished_callback = steps_finished_callback
        self.steps = 0
        self.speed = 0.0
        self.enable = True

    def set_speed(self, speed): # speed may be in range from -1.0 to 1.0
        if speed > 1.0 or speed < -1.0:
            print "speed value out of range"
            return
        if speed == 0:
            self.speed = speed # beware divide by zero error in run()
            return
        if self.backwards_orientation:
            GPIO.output(self.dir_pin, GPIO.LOW if speed > 0.0 else GPIO.HIGH)
        else:
            GPIO.output(self.dir_pin, GPIO.LOW if speed < 0.0 else GPIO.HIGH)
        self.speed = speed

    def set_steps(self, steps):
        if self.steps > 0:
            print "notification from stepper_pulses_general.Channel: calling set_steps() while previous steps are unfinished", self.steps
        self.steps = steps

    def set_enable(self, enable): # enable:[True|False]
        self.enable = enable

    def add_to_queue(self, action, data): #actions: ["set_speed"|"set_steps"|"set_enable"]
        self.queue.put((action, data))

    def run(self):
        while True:
            try:
                action, data = self.queue.get(False)
                if action == "set_speed":
                    self.set_speed(data)
                if action == "set_steps":
                    self.set_steps(data)
                if action == "set_enable":
                    self.set_enable(data)
            except Queue.Empty:
                pass
            if self.enable and self.speed != 0.0 and self.steps > 0:
                GPIO.output(self.gpio_pin, GPIO.LOW)
                time.sleep(period)
                time.sleep(base_pulse_period * (1.0 / self.speed)) # actual sleep period will be longer b/c of processor scheduling
                GPIO.output(self.gpio_pin, GPIO.HIGH)
                time.sleep(period)
                time.sleep(base_pulse_period * (1.0 / self.speed)) # actual sleep period will be longer b/c of processor scheduling
                self.steps -= 1
            else:
                if self.steps == 0 and self.steps_finished_callback:
                    self.steps_finished_callback()
                time.sleep(base_pulse_period)

channels = {}

def init(channels):
    for channel in channels:
        channels[channel.name] = Channel(
            channel["pulse_pin"],
            channel["dir_pin"],
            0.001 if "base_pulse_period" not in channel else channel["base_pulse_period"],
            False if "steps_finished_callback" not in channel else channel["steps_finished_callback"],
            False if "backwards_orientation" not in channel else channel["backwards_orientation"]
        )
        channels[channel.name].start()

# usage:
# channels["channel_name"].set_speed(-0.5)