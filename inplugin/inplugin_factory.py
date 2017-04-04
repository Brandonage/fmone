# A factory to create inplugins

from cpu_inplugin import CpuInPlugin


def getinplugin(plugin_type):
    if plugin_type=="cpu":
        return CpuInPlugin()