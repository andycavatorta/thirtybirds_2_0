import time
import netifaces as ni
import commands
from thirtybirds.Logs.main import Exception_Collector

@Exception_Collector()
class Bip():

	def _ledonoff(self,interval, rep):	
		for x in range(rep):
			commands.getstatusoutput('echo 1 >/sys/class/leds/led0/brightness')
			time.sleep(interval) 
			commands.getstatusoutput('echo 0 >/sys/class/leds/led0/brightness')
			time.sleep(interval)
	def _blinkNumber(self,character):
		character = self.ipAddress[character]
		if character == '.':
			self._ledonoff(0.2,5)
		else:
			self._ledonoff(0.5,character)
		time.sleep(1.8)
	def _startStop(self):
		self._ledonoff(0.1,20)

	def _castInt(self,x):
			if self.ipAddress[x] != '.':
				self.ipAddress[x] = int(self.ipAddress[x])
			else:
				self.ipAddress[x] = self.ipAddress[x]

	def _init(self):
		if commands.getoutput('cat /sys/class/net/eth0/carrier') == '1':
			ni.ifaddresses('eth0')
			self.ipAddress = ni.ifaddresses('eth0')[2][0]['addr']
			print self.ipAddress
		elif commands.getoutput('cat /sys/class/net/wlan0/carrier') == '1':
			ni.ifaddresses('wlan0')
			self.ipAddress = ni.ifaddresses('wlan0')[2][0]['addr']
			print self.ipAddress
		else:
			print "Not connected"
			self._ledonoff(0.1, 30)
		self.ipAddress = list(self.ipAddress)
		print len(self.ipAddress)
		map(self._castInt, range(len(self.ipAddress)))

	def start(self):
		self._init()
		self._startStop()
		time.sleep(2)
		map(self._blinkNumber, range(len(self.ipAddress)))
		time.sleep(2)
		self._startStop()

bip = Bip()