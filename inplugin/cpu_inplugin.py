from inplugin import InPlugin
import psutil
import socket
import time
from sys import platform
from common.funits import Fvalue

class CpuInPlugin(InPlugin):
    def __init__(self,coll_period):
        InPlugin.__init__(self,coll_period)
        if platform=="linux2": ## If we detect is running on the alpine docker container
            psutil.PROCFS_PATH = "/proc_host"

    def collect(self): # here we have to make the loop with coll_period
        cputimes = psutil.cpu_times_percent()
        for name,value in cputimes._asdict().iteritems():
            value = Fvalue(fmetric= "cpu_" + name, fhost=socket.gethostname(), fvalue= value, funit='%',
                           ftime=int(round(time.time() * 1000)),
                           finfo="cpu")
            self.buffer.append(value)

    def pop(self):
        res = self.buffer
        self.buffer = []
        return res



