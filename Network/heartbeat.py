import info
import threading
import time
import zmq

#from thirtybirds_2_0.Logs.main import Exception_Collector

#@Exception_Collector(["check_if_alive","record_heartbeat"])

HEARTBEAT_SEND_PERIOD = 15
HEARTBEAT_TIMEOUT_PERIOD = 20

class Publisher():
    def __init__(self, hostname, timeout = HEARTBEAT_TIMEOUT_PERIOD):
        print "Network.heartbeat.Publisher.__init__", hostname
        self.hostname = hostname
        self.timeout = timeout
        self.last_heartbeat = time.time() - (2 * self.timeout )
    def check_if_alive(self):
        print "Network.heartbeat.Publisher.check_if_alive"
        return True if time.time() - self.timeout < self.last_heartbeat else False
    def record_heartbeat(self):
        print "Network.heartbeat.Publisher.record_heartbeat"
        self.last_heartbeat = time.time()
        
#@Exception_Collector(["check_if_alive","record_heartbeat"])
class Heartbeat(threading.Thread):
    def __init__(self, hostname, pubsub):
        threading.Thread.__init__(self)
        print "Network.heartbeat.Heartbeat.__init__", hostname
        self.topic = "__heartbeat__"
        self.hostname = hostname
        self.pubsub = pubsub
        self.publishers = {}
    def subscribe(self, hostname):
        print "Network.heartbeat.Heartbeat.subscribe", hostname
        self.publishers[hostname] = Publisher(hostname)
    def check_if_alive(self, hostname):
        print "Network.heartbeat.Heartbeat.check_if_alive", hostname
        return self.publishers[hostname].check_if_alive()
    def record_heartbeat(self, hostname):
        print "Network.heartbeat.Heartbeat.record_heartbeat", hostname
        if hostname not in self.publishers:
            self.subscribe(hostname)
        self.publishers[hostname].record_heartbeat()
    def run(self):
        while True: 
            print "Network.heartbeat.Heartbeat.run", self.topic, self.hostname
            self.pubsub.send(self.topic, self.hostname)
            time.sleep(HEARTBEAT_SEND_PERIOD)

def init(hostname, pubsub):
    print "Network.heartbeat.init"
    hb = Heartbeat(hostname, pubsub)
    hb.start()
    return hb
