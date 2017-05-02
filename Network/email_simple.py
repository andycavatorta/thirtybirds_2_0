import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

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

    def send(self, toAddress, subject, body, attachment_path=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.fromAddress
            msg['To'] = toAddress
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            if attachment_path:
                attachment = open(attachment_path, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
                msg.attach(part)

            server = smtplib.SMTP(self.smptServer, self.smtpPort)
            server.starttls()
            server.login(self.fromAddress, self.password)
            server.sendmail(self.fromAddress, toAddress, msg.as_string())
            server.quit()
        except Exception as e:
            print "Exception in email_simple.Send.send", e


def init(fa, pw):
    return Send(fromAddress=fa, password=pw)


"""
write Retrieve class when it's needed

"""
