# Here we include all the units that will be used by the monitoring system, namely values and vector of values
import time

class Fvalue():
    
    def __init__(self, fmetric, fhost, fvalue, ftime, funit=None, finfo=None):
        """

        :param fmetric: the name of the metric
        :param fhost: the name of the host
        :param fvalue: the value of the metric
        :param funit: the unit of the metric
        :param ftime: the time of the metric
        :param finfo: information about the metric
        """
        self.fmetric = fmetric
        self.finf = finfo
        self.fhost = fhost
        self.fvalue = fvalue
        self.funit = funit
        self.ftime = ftime


class Fvector():
    pass