import logging
import smtplib
from email.mime.text import MIMEText
import os

class Errorlog():

	def __init__(self):
		#Logging
		try:
			LOG_PATH = ("%s/Logs")%(os.getcwd())
			print LOG_PATH 
			if not os.path.exists(LOG_PATH):
				print 'Creating directory...'
				os.makedirs(LOG_PATH)
		except Exception as e:
			print "setting default path..."
			LOG_PATH = os.path.dirname(os.path.realpath(__file__))
		self.LOG_FILENAME = "%s/log.csv" % (LOG_PATH)
		self.logger = logging.getLogger("Python Error Log")
		self.logger.setLevel(logging.DEBUG)
		self.ch = logging.FileHandler(self.LOG_FILENAME)
		self.ch.setLevel(logging.DEBUG)
		self.formatter = logging.Formatter("%(asctime)s,%(message)s")
		self.ch.setFormatter(self.formatter)
		self.logger.addHandler(self.ch)

	def loginfo(self, msg):
		self.logger.info(msg)

	def setEmail(self, frm, to, filename, user, pwd, server):
		self.fromaddr = frm
		self.toaddrs  = to
		fp = open(filename, 'rb')
		self.msg = MIMEText(fp.read())
		fp.close()
		self.msg['Subject'] = 'The contents of %s' % filename
		self.msg['From'] = frm
		self.msg['To'] = to
		self.username = user
		self.password = pwd
		self.server = smtplib.SMTP(server)
	def sendEmail(self):
		self.server.starttls()
		self.server.ehlo()
		self.server.login(self.username,self.password)
		self.server.sendmail(self.fromaddr, self.toaddrs, self.msg.as_string())
		self.server.quit()

elog = Errorlog()