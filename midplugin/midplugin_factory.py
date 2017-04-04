# A factory to create midplugins
from inout_midplugin import InOutMidPlugin


def getmidplugin(plugin_type):
    if plugin_type=="inout":
        return InOutMidPlugin()