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
#from thirtybirds_2_0.Logs.main import Exception_Collector

#@Exception_Collector("pubsub_callback")
class Manager(threading.Thread):
    def __init__(
            self, 
            hostname,
            role,
            #specified_interface_name,
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
        print "Network.Manager.__init__"
        self.hostname = hostname
        self.role = role
        #self.specified_interface_name = specified_interface_name
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
        #print "initializing self.discovery"
        # temp test block start
        #print "self.hostname ", self.hostname
        #print "self.role ", self.role
        #print "discovery_multicastGroup ", discovery_multicastGroup
        #print "discovery_multicastPort ", discovery_multicastPort
        #print "discovery_responsePort ", discovery_responsePort
        #print "self.local_discovery_status_callback ", self.local_discovery_status_callback
        # temp test block end
        self.discovery = discovery.init(
            self.hostname,
            self.role,
            #self.specified_interface_name,
            discovery_multicastGroup, 
            discovery_multicastPort, 
            discovery_responsePort, 
            self.local_discovery_status_callback
            )
        #print "DONE with self.discovery"
        #print "initializing self.pubsub"
        self.pubsub = pubsub.init(
            self.hostname,
            #self.specified_interface_name,
            pubsub_pubPort, 
            self.pubsub_callback,
            self.local_discovery_status_callback
            )
        #print "initializing self.heartbeat"
        self.heartbeat = heartbeat.init(
            self.hostname,
            self.pubsub
            )

    def local_discovery_status_callback(self,msg):
        #print "Network.Manager.local_discovery_status_callback", repr(msg)
        #print "local_discovery_status_callback", repr(msg)
        time.sleep(0.1)
        if hasattr(self, "heartbeat"):
            if msg["status"] == "device_discovered":
                self.heartbeat.subscribe(msg["hostname"])
                self.pubsub.connect_to_publisher(msg["hostname"], msg["ip"], self.pubsub_pubPort)
                self.pubsub.subscribe_to_topic("__heartbeat__")
                # NOT_THREAD_SAFE
                self.publishers[msg["hostname"]] = {"connected":False} # connected is not redundant here.  we use its state to detect changes to heartbeat status
            self.status_callback(msg)
        #else:
            #print 'else'

    def local_pubsub_status_callback(self,msg):
        #print "Network.Manager.local_pubsub_status_callback", msg
        self.status_callback(msg)

    def local_heartbeat_status_callback(self,msg):
        #print "Network.Manager.local_heartbeat_status_callback", msg
        #print "local_heartbeat_status_callback", msg
        self.status_callback(msg)

    def pubsub_callback(self, msg, host):
        #print "Network.Manager.pubsub_callback", msg, host
        if msg == "__heartbeat__":
            self.heartbeat.record_heartbeat(host)
        else:
            self.message_callback((msg, host))
            #print "pubsub_callback", msg, host

    def subscribe_to_topic(self, topic):
        #print "Network.Manager.subscribe_to_topic", topic
        self.pubsub.subscribe_to_topic(topic)

    def send(self, topic, msg):
        #print "Network.Manager.send", topic, msg
        self.pubsub.send(topic, msg)

    def send_blob(self, topic, msg):
        #print "Network.Manager.send_blob", topic, msg
        self.pubsub.send_blob(topic, msg)

    def run(self):
        while True:
            for publisher_hostname,val in self.publishers.items():# loop through all known publishers, check live status
                alive = self.heartbeat.check_if_alive(publisher_hostname)
                #print "Network.Manager.run", publisher_hostname, alive
                if self.publishers[publisher_hostname]["connected"] != alive: # detect a change is heartbeat status
                    self.publishers[publisher_hostname]["connected"] = alive
                    if alive == False and self.role == "caller": # if a publisher has just come back online.
                        self.discovery.begin()
            time.sleep(15)

def init(
        hostname,
        role,
        #specified_interface_name,
        discovery_multicastGroup,
        discovery_multicastPort,
        discovery_responsePort,
        pubsub_pubPort,
        message_callback,
        status_callback
    ):
    r = "caller" if role == "client" else "responder"
    print "Network.Manager.init", hostname
    m = Manager(
        hostname,
        r,
        #specified_interface_name,
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
