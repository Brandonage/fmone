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
        self.finfo = finfo
        self.fhost = fhost
        self.fvalue = fvalue
        self.funit = funit
        self.ftime = ftime

    @classmethod
    def fromdict(cls,datadict):
        """Create a Fvalue from a dict value. Useful when reading serialised jsons
           It is a class method so it's able to return itself
           :param datadict: a dict holding the values of the fvalue
        """
        return cls(fmetric=datadict.get('fmetric'),
                   fhost=datadict.get('fhost'),
                   fvalue=datadict.get('fvalue'),
                   ftime=datadict.get('ftime'),
                   funit=datadict.get('funit'),
                   finfo=datadict.get('finfo'))


class Fvector():
    pass