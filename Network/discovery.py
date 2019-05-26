#########################################
######## IMPORTS, PATHS, GLOBALS ########
#########################################

import info
import json
import socket
import struct
import threading
import time
import yaml
import zmq

#from thirtybirds_2_0.Logs.main import Exception_Collector

from thirtybirds_2_0.Network.info import init as network_info_init
network_info = network_info_init()

CALLER_PERIOD = 10

#####################
##### RESPONDER #####
#####################

#@Exception_Collector()
class Responder(threading.Thread):
    def __init__(self, listener_grp, listener_port, response_port, localIP, callback):
        threading.Thread.__init__(self)
        print "Network.discovery.Responder.__init__"
        self.listener_port = listener_port
        self.response_port = response_port
        self.localIP = localIP
        self.callback = callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((listener_grp, listener_port))
        self.mreq = struct.pack("4sl", socket.inet_aton(listener_grp), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
        self.IpTiming = {}
    def response(self, remoteIP, msg_json): # response sends the local IP to the remote device
        print "Network.discovery.Responder.response", remoteIP, msg_json
        if self.IpTiming.has_key(remoteIP):
            if self.IpTiming[remoteIP] + (CALLER_PERIOD * 2) > time.time():
                return
        else:
            self.IpTiming[remoteIP] = time.time()
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        socket.connect("tcp://%s:%s" % (remoteIP,self.response_port))
        socket.send(msg_json)
        socket.close()
    def run(self):
        while True:
                msg_json = self.sock.recv(1024)
                print "Network.discovery.Responder.run", msg_json
                msg_d = yaml.safe_load(msg_json)
                remoteIP = msg_d["ip"]
                msg_d["status"] = "device_discovered"
                if self.callback:
                    resp_d = self.callback(msg_d)
                resp_json = json.dumps( {"ip":self.localIP,"hostname":socket.gethostname()})
                self.response(remoteIP,resp_json)

##################
##### CALLER #####
##################

class CallerSend(threading.Thread):
    def __init__(self, localHostname, localIP, mcast_grp, mcast_port):
        threading.Thread.__init__(self)
        print "Network.discovery.CallerSend.run", localHostname, localIP, mcast_grp, mcast_port
        self.mcast_grp = mcast_grp
        self.mcast_port = mcast_port
        self.mcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mcast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.msg_d = {"ip":localIP,"hostname":localHostname}
        self.msg_json = json.dumps(self.msg_d)
        self.mcast_msg = self.msg_json
        self.active = True
    def set_active(self,val):
        # NOT_THREAD_SAFE
        print "Network.discovery.CallerSend.set_active", val
        self.active = val
    def run(self):
        while True:
            if self.active == True:
                print "Network.discovery.CallerSend.run"
                self.mcast_sock.sendto(self.mcast_msg, (self.mcast_grp, self.mcast_port))
            time.sleep(CALLER_PERIOD)

class CallerRecv(threading.Thread):
    def __init__(self, recv_port, callback, callerSend):
        threading.Thread.__init__(self)
        print "Network.discovery.CallerRecv.__init__"
        self.callback = callback
        self.callerSend = callerSend
        self.listen_context = zmq.Context()
        self.listen_sock = self.listen_context.socket(zmq.PAIR)
        self.listen_sock.bind("tcp://*:%d" % recv_port)
        self.msg = ""
        self.server_ip = ""
    def run(self):
        while True:
            msg_json = self.listen_sock.recv()
            print "Network.discovery.CallerRecv.run", msg_json
            msg_d = yaml.safe_load(msg_json)
            msg_d["status"] = "device_discovered"
            self.callerSend.set_active(False)
            if self.callback:
                self.callback(msg_d)

###################
##### WRAPPER #####
###################
class Discovery():
    def __init__(
            self,
            hostname,
            role,
            #specified_interface_name,
            multicastGroup,
            multicastPort, 
            responsePort,
            status_callback
        ):
        print "Network.discovery.Discovery.__init__", hostname
        self.role = role
        self.hostname = hostname
        #self.specified_interface_name = specified_interface_name
        self.multicastGroup = multicastGroup
        self.multicastPort = multicastPort
        self.responsePort = responsePort
        self.status_callback = status_callback
        self.server_ip = ""
        self.status = "" 

        if self.role == "caller":
            self.callerSend = CallerSend(
                self.hostname, 
                #network_info.getLocalIp(self.specified_interface_name), 
                multicastGroup, 
                multicastPort
            )
            self.callerRecv = CallerRecv(
                responsePort, 
                self.status_callback, 
                self.callerSend
            )
            self.callerRecv.start()
            self.callerSend.start()

        if self.role == "responder":
            self.responder = Responder(
                self.multicastGroup,
                self.multicastPort, 
                self.responsePort, 
                network_info.getLocalIp(), 
                self.status_callback
            )
            self.responder.start()

        #logger("trace","Thirtybirds.Network.discovery:Discovery","initialized as %s" % (self.role),None)
        

    def begin(self):
        print "Network.discovery.Discovery.begin"
        self.callerSend.set_active(True)

    def end(self):
        print "Network.discovery.Discovery.end"
        self.callerSend.set_active(False)

    def get_status(self):
        print "Network.discovery.Discovery.get_status"
        return self.status

    def get_server_ip(self):
        print "Network.discovery.Discovery.get_server_ip"
        return self.server_ip

def init(
        hostname,
        role,
        #specified_interface_name,
        multicastGroup,
        multicastPort, 
        responsePort,
        status_callback
    ):
    print "Network.discovery.init"
    return Discovery(
        hostname,
        role,
        #specified_interface_name,
        multicastGroup,
        multicastPort, 
        responsePort,
        status_callback
    )
