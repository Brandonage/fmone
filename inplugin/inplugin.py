# The interface that has to be implemented by an InPlugin
from threading import Thread
import time

class InPlugin(Thread):
    def __init__(self,coll_period):
        Thread.__init__(self)
        self.daemon = True
        self.buffer = []
        self.coll_period = coll_period
        pass

    def run(self):
        while True:
            time1 = time.time()
            self.collect()
            time2 = time.time()
            timediff = time2-time1
            time.sleep(self.coll_period - timediff)

    def collect(self):
        pass

    def pop(self):
        pass
