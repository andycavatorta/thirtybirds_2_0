import Queue
import RPi.GPIO as GPIO
import threading
import time

class Motor(threading.Thread):
    def __init__(
            self, 
            name,
            pulse_pin, 
            dir_pin, 
            base_pulse_period = 0.001, 
            status_callback = False, 
            backwards_orientation = False
        ):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.name = name
        self.pulse_pin = pulse_pin
        self.dir_pin = dir_pin
        self.base_pulse_period = base_pulse_period
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pulse_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.pulse_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)
        self.backwards_orientation = backwards_orientation
        self.status_callback = status_callback
        self.steps = 0
        self.steps_cursor = 0
        self.direction = True
        self.speed = 0.0
        self.enable = True
 

    def set_speed(self, speed): # valid values for speed are 0.0-1.0
        if 0.0 <= speed <= 1.0:
            self.speed = speed
        else:
            print "stepper_pulses.Motor speed out of range", speed

    def set_steps(self, steps): # valid value for steps is any integer
        self.steps = abs(int(steps))
        self.direction = True if steps > 0 else False
        self.steps_cursor = 0
        #if self.backwards_orientation:
        #    GPIO.output(self.dir_pin, GPIO.LOW if self.direction else GPIO.HIGH)
        #else:
        #    GPIO.output(self.dir_pin, GPIO.LOW if self.direction else GPIO.HIGH)

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
                    self.status_callback(self.name, "started", None)
                if action == "set_enable":
                    self.set_enable(data)
            except Queue.Empty:
                pass
            if self.enable and self.speed > 0.0 and self.steps > self.steps_cursor:
                GPIO.output(self.pulse_pin, GPIO.LOW)
                time.sleep(self.base_pulse_period * (1.0 / self.speed)) # actual sleep period will be longer b/c of processor scheduling
                GPIO.output(self.pulse_pin, GPIO.HIGH)
                time.sleep(self.base_pulse_period * (1.0 / self.speed)) # actual sleep period will be longer b/c of processor scheduling
                self.steps_cursor += 1 
                #if self.steps_cursor%10 == 0:
                self.status_callback(self.name, "steps_cursor", self.steps_cursor)
                if self.steps == self.steps_cursor:
                    self.status_callback(self.name, "finished", True)
            else:
                time.sleep(self.base_pulse_period)

motors = {} # global placeholder

def init(motor_settings):
    global motors
    for motor_name in motor_settings:
        motors[motor_name] = Motor(
            motor_name,
            motor_settings[motor_name]["pulse_pin"], 
            motor_settings[motor_name]["dir_pin"], 
            motor_settings[motor_name]["base_pulse_period"], 
            motor_settings[motor_name]["status_callback"], 
            motor_settings[motor_name]["backwards_orientation"]
            )
        motors[motor_name].start()

def set(motor_name, action, data):
    if motor_name not in motors:
        print "Channel name not found:", motor_name
        return
    if action == "steps":
        motors[motor_name].add_to_queue( "set_steps", data)
        return
    if action == "speed":
        motors[motor_name].add_to_queue( "set_speed", data)
        return
    if action == "enable":
        motors[motor_name].add_to_queue( "set_enable", data)
        return

