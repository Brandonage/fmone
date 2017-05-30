from inplugin import InPlugin
import psutil
import socket
import time
from sys import platform
from common.funits import Fvalue

class HostMetricsInPlugin(InPlugin):
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
        cpustats = psutil.cpu_stats()
        for name,value in cpustats._asdict().iteritems():
            value = Fvalue(fmetric= "cpu_" + name, fhost=socket.gethostname(), fvalue= value, funit='nops',
                           ftime=int(round(time.time() * 1000)),
                           finfo="cpustats")
            self.buffer.append(value)
        memory = psutil.virtual_memory()
        for name,value in memory._asdict().iteritems():
            value = Fvalue(fmetric= "mem_" + name, fhost=socket.gethostname(), fvalue= value, funit='bytes',
                           ftime=int(round(time.time() * 1000)),
                           finfo="mem")
            self.buffer.append(value)
        disk = psutil.disk_io_counters()
        for name,value in disk._asdict().iteritems():
            value = Fvalue(fmetric= "disk_" + name, fhost=socket.gethostname(), fvalue= value, funit='bytes',
                           ftime=int(round(time.time() * 1000)),
                           finfo="disk")
            self.buffer.append(value)
        network = psutil.net_io_counters()
        for name,value in network._asdict().iteritems():
            value = Fvalue(fmetric= "net_" + name, fhost=socket.gethostname(), fvalue= value, funit='bytes',
                           ftime=int(round(time.time() * 1000)),
                           finfo="net")
            self.buffer.append(value)







