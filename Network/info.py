import netifaces
import urllib2
import socket

#from thirtybirds_2_0.Logs.main import Exception_Collector

#@Exception_Collector()
class Info():
    def __init__(self):
        pass
    def getLocalIp(self):
        ifaces = netifaces.interfaces()
        for iface in ifaces:
            try:
                ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
                if ip[0:3] != "127":
                    return ip
            except Exception as e:
                pass
        return False

    def getGlobalIp(self):
        try:
            return urllib2.urlopen("http://icanhazip.com", timeout=5).read().strip()
        except Exception as e:
            return False

    def getHostName(self):
        try:
            return socket.gethostname()
        except Exception as e:
            return False

    def getOnlineStatus(self):
        r = self.getLocalIp()
        return False if r==False else True

def init():
    return Info()

