import commands
import re
from Queue import Queue, Empty
import subprocess
import threading
import time
from threading import Thread
import traceback
import urllib
import urllib2


class ReverseTunnel(threading.Thread):
    def __init__(self, retry_wait, ping_url):
        self.retry_wait = retry_wait
        self.ping_url = ping_url

        threading.Thread.__init__(self)
    def run(self):
        while True:
            try:
                result_str = ""
                p = subprocess.Popen(["sudo", "-u", "pi", "ssh", "-v", "-o", "StrictHostKeyChecking=no", "-N", "-R 0:localhost:22", "andy@web143.webfaction.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(30)
                nbsr = NonBlockingStreamReader(p.stderr)
                nbsr.start()
                while True:
                    output = nbsr.readline(0.1)
                    if not output:
                        print '[No more data]'
                        break
                    else:
                        result_str += output

                if result_str.find("REMOTE HOST IDENTIFICATION HAS CHANGED") > -1:
                    print "REMOTE HOST IDENTIFICATION HAS CHANGED"
                else:
                    port = int(result_str.split()[result_str.split().index("Allocated")+2])
                    self.postPing(port)
                    p.wait()
            except Exception as e:
                print "error in reverse_ssh_tunnel", e, traceback.print_exc()
            time.sleep(self.retry_wait)

    def postPing(self, remote_port):
        try:
            #response = urllib2.urlopen(self.ping_url, urllib.urlencode({"remote_port": remote_port}))
            request = urllib2.Request(self.ping_url)
            request.addheaders = [('Authorization', self.auth_token_str)]
            #request.add_header('Authorization', self.auth_token_str)
            response = urllib2.urlopen(
                request,
                urllib.urlencode({"remote_port": remote_port})
                )
            html = response.read()

            #print "ReverseTunnel postPing 4"
        except Exception as e:
            print "error in reverse_ssh_tunnel", e, traceback.print_exc()

class NonBlockingStreamReader(threading.Thread):
    def __init__(self, stream):
        self.stream = stream
        self.queue = Queue()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                line = self.stream.readline()
                if line:
                    print time.time(), "debug | reverse_ssh_tunnel | NonBlockingStreamReader line =", line
                    self.queue.put(line)

            except Exception as e:
                print "error in reverse_ssh_tunnel", e, traceback.print_exc()

    def readline(self, timeout = None):
        try:
            return self.queue.get(block = timeout is not None, timeout = timeout)
        except Empty:
            return None
