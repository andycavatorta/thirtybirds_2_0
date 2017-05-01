import info
import os
import sys
import threading
import time
import traceback
import zmq

from thirtybirds.Logs.main import Exception_Collector

from thirtybirds.Network.info import init as network_info_init
network_info = network_info_init()

@Exception_Collector()
class Subscription():
    def __init__(self, hostname, remote_ip, remote_port):
        self.hostname = hostname
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.connected = False
        
@Exception_Collector("send")
class PubSub(threading.Thread):
    def __init__(self, hostname, publish_port, recvCallback, netStateCallback):
        threading.Thread.__init__(self)
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
        print topic, msg
        self.pub_socket.send_string("%s %s" % (topic, msg))

    def connect_to_publisher(self, hostname, remote_ip, remote_port):
            if hostname not in self.subscriptions:
                self.subscriptions[hostname] = Subscription(hostname, remote_ip, remote_port)
                self.sub_socket.connect("tcp://%s:%s" % (remote_ip, remote_port))

    def subscribe_to_topic(self, topic):
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe_from_topic(self, topic):
            topic = topic.decode('ascii')
            self.sub_socket.setsockopt(zmq.UNSUBSCRIBE, topic)

    def run(self):
        while True:
            incoming = self.sub_socket.recv()
            topic, msg = incoming.split(' ', 1)
            self.recvCallback(topic, msg)

def init(hostname, publish_port, recvCallback, netStateCallback):
    print 'inside pubsub init'
    ps = PubSub(hostname, publish_port, recvCallback, netStateCallback)
    ps.start()
    return ps
