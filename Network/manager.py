"""
manager.py initializes and coordinates the interconnected network functions: discovery, pubsub, and heartbeat

One should be able to simply invoke these 

"""

#########################################
######## IMPORTS, PATHS, GLOBALS ########
#########################################

import discovery
import heartbeat
import pubsub
import threading
import time
from thirtybirds.Logs.main import Exception_Collector

@Exception_Collector("pubsub_callback")
class Manager(threading.Thread):
    def __init__(
            self, 
            hostname,
            role,
            discovery,
            pubsub,
            heartbeat,
            discovery_multicastGroup,
            discovery_multicastPort,
            discovery_responsePort,
            pubsub_pubPort,
            message_callback,
            status_callback
        ):
        threading.Thread.__init__(self)

        self.hostname = hostname
        self.role = role
        self.discovery_multicastGroup = discovery_multicastGroup
        self.discovery_multicastPort = discovery_multicastPort
        self.discovery_responsePort = discovery_responsePort
        self.pubsub_pubPort = pubsub_pubPort
        self.message_callback = message_callback
        self.status_callback = status_callback
        self.server_ip = ""
        self.publishers = {}
        #self.connected = False
        # initialize discovery, pubsub, heartbeat
        print "initializing self.discovery"
        self.discovery = discovery.init(
            self.hostname,
            self.role,
            discovery_multicastGroup, 
            discovery_multicastPort, 
            discovery_responsePort, 
            self.local_discovery_status_callback
            )
        print "initializing self.pubsub"
        self.pubsub = pubsub.init(
            self.hostname,
            pubsub_pubPort, 
            self.pubsub_callback,
            self.local_discovery_status_callback
            )
        print "initializing self.heartbeat"
        self.heartbeat = heartbeat.init(
            self.hostname,
            self.pubsub
            )

    def local_discovery_status_callback(self,msg):
        #print "local_discovery_status_callback", repr(msg)
        time.sleep(2)
        if hasattr(self, "heartbeat"):
            print 'in'
            if msg["status"] == "device_discovered":
                self.heartbeat.subscribe(msg["hostname"])
                self.pubsub.connect_to_publisher(msg["hostname"], msg["ip"], self.pubsub_pubPort)
                self.pubsub.subscribe_to_topic("__heartbeat__")
                self.publishers[msg["hostname"]] = {"connected":False} # connected is not redundant here.  we use its state to detect changes to heartbeat status
            self.status_callback(msg)
        else:
            print 'else'

    def local_pubsub_status_callback(self,msg):
        print "local_pubsub_status_callback", msg
        self.status_callback(msg)

    def local_heartbeat_status_callback(self,msg):
        #print "local_heartbeat_status_callback", msg
        self.status_callback(msg)

    def pubsub_callback(self, msg, host):
        if msg == "__heartbeat__":
            self.heartbeat.record_heartbeat(host)
        else:
            self.message_callback((msg, host))
            #print "pubsub_callback", msg, host

    def subscribe_to_topic(self, topic):
        self.pubsub.subscribe_to_topic(topic)

    def send(self, topic, msg):
        self.pubsub.send(topic, msg)

    def run(self):
        while True:
            for publisher_hostname,val in self.publishers.items():# loop through all known publishers, check live status
                alive = self.heartbeat.check_if_alive(publisher_hostname)
                if self.publishers[publisher_hostname]["connected"] != alive: # detect a change is heartbeat status
                    self.publishers[publisher_hostname]["connected"] = alive
                    if alive: # if a publisher has just come back online.
                        pass
                        #self.logger("trace","Thirtybirds.Network.manager:Manager","publisher %s connected" % (publisher_hostname),None)
                    else: # if a publisher has just gone offline
                        #self.logger("trace","Thirtybirds.Network.manager:Manager","publisher %s disconected" % (publisher_hostname),None)
                        pass
                        if self.role == "caller":
                            #self.logger("trace","Thirtybirds.Network.manager:Manager","starting discovery",None)
                            self.discovery.begin()
                        #else: # if role == "responder"
                        #    self.logger("trace","Thirtybirds.Network.manager:Manager","lisening for new connection from %s" % (publisher_hostname),None)
            time.sleep(2)

def init(
        hostname,
        role,
        discovery_multicastGroup,
        discovery_multicastPort,
        discovery_responsePort,
        pubsub_pubPort,
        message_callback,
        status_callback
    ):
    r = "caller" if role == "client" else "responder"
    m = Manager(
        hostname,
        r,
        discovery,
        pubsub,
        heartbeat,
        discovery_multicastGroup,
        discovery_multicastPort,
        discovery_responsePort,
        pubsub_pubPort,
        message_callback,
        status_callback
    )
    m.start()
    return m
