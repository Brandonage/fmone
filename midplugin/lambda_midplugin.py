from midplugin import MidPlugin
from operator import attrgetter
from itertools import groupby


class LambdaMidPlugin(MidPlugin):
    def __init__(self, func):
        """
        This plugin will provide flexibility when summarising the data of a given key fmetric
        :param func: a function that we want to apply to summarise a list of fvalues before pushing out the data
        The function MUST return and Fvalue. An example of a function would be 
        
        from common.funits import Fvalue
        def average_fvalues(list_of_fvalues):
            fhost = "Summary of several hosts"
            finfo = list_of_fvalues[0].finfo
            fmetric = list_of_fvalues[0].fmetric
            ftime = sum([f.ftime for f in list_of_fvalues]) / len(list_of_fvalues)
            funit = list_of_fvalues[0].funit
            fvalue = sum([f.fvalue for f in list_of_fvalues]) / float(len(list_of_fvalues))
            return Fvalue(fmetric, fhost, fvalue, ftime, funit, finfo)
        """
        MidPlugin.__init__(self)
        self.func = func

    def refine(self, listoffvalues):
        def transform_group_to_fvalue(list_of_fvalues):
            """
            Necesary to construct the summary fvalue object
            :param list_of_fvalues: This is a list of fvalues
            :return: it returns a new fvalue after applying self.func to the group
            """
            return self.func(list_of_fvalues)
        # we group the list of f values by their key, in this case fmetric TODO: The key can be a parameter
        # and we put all the groups in a list of lists
        list_of_lists_fvalues = [list(g) for k, g in groupby(sorted(listoffvalues, key=attrgetter('fmetric')),
                                                         key=attrgetter('fmetric'))]
        # summarise each of the groups of fvalues to a single fvalue
        return map(transform_group_to_fvalue, list_of_lists_fvalues)
