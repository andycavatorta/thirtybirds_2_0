#############################################
##### MODULES, EVENIRONMENT AND GLOBALS #####
#############################################

import os
#import time
import sys
import traceback
import multiprocessing
import time

BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
COMMON_PATH = "%s/common/" % (BASE_PATH )
DEVICES_PATH = "%s/client/devices/" % (BASE_PATH )
SERVER_PATH = "%s/server/" % (BASE_PATH )
STORE_PATH = "%s/store/" % SERVER_PATH

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

import signalOutput

CRLF = "\n"

class CommandLine_Funcs(multiprocessing.Process):
  def __init__(self,conn):
    multiprocessing.Process.__init__(self) 
    self.conn = conn
    print self

  def run(self):
    pass

  def display(self,msg):
    self.msg = msg
    sys.stdout.write("%s"%(self.msg))

  def menuChannel(self):
    while True:
      self.params = {}
      self.display("Select a channel (0-23):")
      self.input_raw = sys.stdin.readline()
      try:
        self.input_int = int(self.input_raw[:-1])
        if 0<= self.input_int <=23:
          self.params["channel"] = self.input_int
          self.menuFunction(self.params)
      except Exception as e:
        print "menuChannel:please enter a number between 0 and 23:"

  def menuFunction(self,params):
    self.params = params
    self.fmap = {
      "s":self.menuSquareWave,
      "d":self.menuDigital,
      "p":self.menuPulse,
      # "v":self.menuValues
    }  
    self.goodValue = False
    while self.goodValue == False:
      self.display("Select a function:\n")
      self.display("  s - Square Wave\n")
      self.display("  d - Digital (on/off)\n")
      self.display("  p - Pulse \n")
      # self.display("  v - Channel Values \n")
      input = sys.stdin.readline()
      try:
        self.fmap[input[:-1]](self.params)
        self.goodValue = True
      except Exception as e:
        print "menuFunction: invalid value:", input
        print traceback.print_exc()

  def menuSquareWave(self,params):
    self.params = params
    self.params["function"] = "square wave"
    self.menuFreq(self.params)
    self.menuPWM(self.params)
    self.conn.send(self.params)

  def menuDigital(self,params):
    self.params = params
    self.params["function"] = "digital"
    self.goodValue = False
    while self.goodValue == False:
      self.display("Enter an on/off value (0 or 1):")
      self.input_raw = sys.stdin.readline()
      try:
        self.input_int = int(self.input_raw[:-1])
        if self.input_int in (0,1):
          self.params["bool"] = self.input_int
          self.conn.send(self.params)
          self.goodValue = True
      except Exception as e:
        print "menuDigital:invalid value:", input
        print traceback.print_exc()
    return 

  def menuPulse(self,params):
    self.params = params
    self.params["function"] = "pulse"
    self.goodValue = False
    while self.goodValue == False:
      self.display("Enter a pulse length in seconds (precise to two decimal places):")
      self.input_raw = sys.stdin.readline()

      try:
        self.input_f = float(self.input_raw[:-1])
        if 0.0 <= self.input_f:
          self.params["pulselength"] = self.input_f
          self.conn.send(self.params)
          self.goodValue = True
      except Exception as e:
        print "menuPulse:invalid value:", input
        print traceback.print_exc()
    return 

  # def menuValues(self,params):
  #   self.params = params
  #   self.states = signalOutput.channels.getStates()
  #   for i in range(len(self.states)):
  #     print "ch:", i, self.states[i][0],"Hz,", self.states[i][1], "%"
  #   #print states

  def menuFreq(self,params):
    self.params = params
    self.goodValue = False
    while self.goodValue == False:
      self.display("Enter a frequency in Hz (%f-%f):" % (signalOutput.FREQ_MIN,signalOutput.FREQ_MAX))
      self.input_raw = sys.stdin.readline()
      try:
        self.input_f = float(self.input_raw[:-1])
        if signalOutput.FREQ_MIN <= self.input_f <= signalOutput.FREQ_MAX:
          self.params["frequency"] = self.input_f
          self.goodValue = True
          self.osc_bin_str = ('{0:017b}'.format(int(signalOutput.FPGA_CLOCK_SPEED_DIVIDED / self.input_f)))[::-1]
          print self.input_f, "Hz rounded to", signalOutput.FPGA_CLOCK_SPEED_DIVIDED / int(self.osc_bin_str[::-1], 2), "Hz"

      except Exception as e:
        print "menuFreq:invalid value:", input
        print traceback.print_exc()
    return 
    
  def menuPWM(self,params):
    self.params = params
    self.goodValue = False
    while self.goodValue == False:
      self.display("Enter a duty cycle value (0.0-100.0):")
      self.input_raw = sys.stdin.readline()
      try:
        self.input_f = float(self.input_raw[:-1])
        if 0.0 <= self.input_f <= 100.0:
          self.params["duty cycle"] = self.input_f
          self.goodValue = True
      except Exception as e:
        print "menuPWM:invalid value:", input
    return 