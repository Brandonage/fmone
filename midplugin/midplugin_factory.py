# A factory to create midplugins
from inout_midplugin import InOutMidPlugin
from lambda_midplugin import LambdaMidPlugin
from common.funits import Fvalue

# We can keep here for the moment the different functions that will be passed to the LambdaMidPlugin
# Possibly, this is meant to be transferred to a different module
def average_fvalues(list_of_fvalues):
    fhost = "Summary of several hosts"
    finfo = list_of_fvalues[0].finfo
    fmetric = list_of_fvalues[0].fmetric
    ftime = sum([f.ftime for f in list_of_fvalues]) / len(list_of_fvalues)
    funit = list_of_fvalues[0].funit
    fvalue = sum([f.fvalue for f in list_of_fvalues]) / float(len(list_of_fvalues))
    return Fvalue(fmetric, fhost, fvalue, ftime, funit, finfo)

#

def getmidplugin(plugin_type):
    if plugin_type=="inout":
        return InOutMidPlugin()
    if plugin_type=="average":
        return LambdaMidPlugin(average_fvalues)