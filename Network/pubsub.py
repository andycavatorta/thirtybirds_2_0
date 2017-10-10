import info
import os
import sys
import threading
import time
import traceback
import zmq

#from thirtybirds_2_0.Logs.main import Exception_Collector

from thirtybirds_2_0.Network.info import init as network_info_init
network_info = network_info_init()

#@Exception_Collector()
class Subscription():
    def __init__(self, hostname, remote_ip, remote_port):
        print "Network.pubsub.Subscription.__init__",hostname, remote_ip, remote_port
        self.hostname = hostname
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.connected = False
        
#@Exception_Collector("send")
class PubSub(threading.Thread):
    def __init__(self, hostname, publish_port, recvCallback, netStateCallback):
        threading.Thread.__init__(self)
        print "Network.pubsub.PubSub.__init__", hostname, publish_port
        self.publish_port = publish_port
        self.recvCallback = recvCallback 
        self.netStateCallback = netStateCallback 
        self.hostname = hostname
        self.ip = network_info.getLocalIp()
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind("tcp://*:%s" % publish_port)
        self.sub_socket = self.context.socket(zmq.SUB)
        self.subscriptions = {}

    def send(self, topic, msg):
        print "Network.pubsub.PubSub.send", topic, msg
        #if topic != "__heartbeat__":
        #    print topic, msg
        self.pub_socket.send_string("%s %s" % (topic, msg))

    def send_blob(self, topic, msg):
        print "Network.pubsub.PubSub.send_blob", topic, msg
        if topic != "__heartbeat__":
            print topic, '%d byte blob' % len(msg)
        self.pub_socket.send_string("%s %s" % (topic, msg))

    def connect_to_publisher(self, hostname, remote_ip, remote_port):
        print "Network.pubsub.PubSub.connect_to_publisher", hostname, remote_ip, remote_port
        if hostname not in self.subscriptions:
            self.subscriptions[hostname] = Subscription(hostname, remote_ip, remote_port)
            self.sub_socket.connect("tcp://%s:%s" % (remote_ip, remote_port))

    def subscribe_to_topic(self, topic):
        print "Network.pubsub.PubSub.subscribe_to_topic", topic
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe_from_topic(self, topic):
        print "Network.pubsub.PubSub.unsubscribe_from_topic", topic
        topic = topic.decode('ascii')
        self.sub_socket.setsockopt(zmq.UNSUBSCRIBE, topic)

    def run(self):
        while True:
            print "Network.pubsub.PubSub.run"
            incoming = self.sub_socket.recv()
            topic, msg = incoming.split(' ', 1)
            self.recvCallback(topic, msg)

def init(hostname, publish_port, recvCallback, netStateCallback):
    print "Network.pubsub.init",hostname, publish_port
    ps = PubSub(hostname, publish_port, recvCallback, netStateCallback)
    ps.start()
    return ps
