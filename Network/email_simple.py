

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 

class Send():
    def __init__(self,smptServer='smtp.gmail.com', smtpPort=587, fromAddress="", password=""):
    	try:
	        self.safety = True
	        self.messages = []
	        self.smptServer = smptServer
	        self.smtpPort = smtpPort
	        self.fromAddress = fromAddress
	        self.password = password
	    except Exception as e:
	    	print "Exception in email_simple.Send.__init", e

    def send(self, toAddress, subject, body):
    	try:
			msg = MIMEMultipart()
			msg['From'] = self.fromAddress
			msg['To'] = toAddress
			msg['Subject'] = subject
			msg.attach(MIMEText(body, 'plain'))
			server = smtplib.SMTP(self.smptServer, self.smtpPort)
			server.starttls()
			server.login(self.fromAddress, self.password)
			server.sendmail(self.fromAddress, toAddress, msg.as_string())
			server.quit()
	    except Exception as e:
	    	print "Exception in email_simple.Send.send", e

"""

write Retrieve class when it's needed

"""


