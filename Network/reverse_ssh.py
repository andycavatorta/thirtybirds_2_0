from threading import Thread
from Queue import Queue, Empty

class NonBlockingStreamReader:
    def __init__(self, stream):
        self._s = stream
        self._q = Queue()
        def _populateQueue(stream, queue):
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream
        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream
    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass

from subprocess import Popen, PIPE
from time import sleep
p = Popen(["sudo", "-u", "pi", "ssh", "-v", "-o", "StrictHostKeyChecking=no", "-N", "-R 0:localhost:22", "ubuntu@api.callmeishmael.com"],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
nbsr = NonBlockingStreamReader(p.stderr)
sleep(5)
while True:
    output = nbsr.readline(0.1)
    if not output:
        print '[No more data]'
        break
    print output