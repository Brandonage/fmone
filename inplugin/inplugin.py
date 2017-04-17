# The interface that has to be implemented by an InPlugin
from threading import Thread
import time

class InPlugin(Thread):
    "It inherits from the Thread object and overrides the run method to run as a thread"
    def __init__(self,coll_period):
        Thread.__init__(self)
        self.daemon = True
        self.buffer = [] # This buffer must always contain Fvalues
        self.coll_period = coll_period
        pass

    def run(self):
        "this is the continuous loop that is going to run as a separate thread"
        while True:
            time1 = time.time()
            self.collect()
            time2 = time.time()
            timediff = time2-time1
            time.sleep(self.coll_period - timediff)

    def collect(self):
        pass

    def pop(self):
        res = self.buffer
        self.buffer = []
        return res
