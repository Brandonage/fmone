# A factory to create outplugins
from file_outplugin import FileOutPlugin


def getoutplugin(plugin_type,**args):

    if plugin_type=="file":
        filepath = args.get("outfilepath")
        if not isinstance(filepath,str):
            raise ValueError("Wrong parameters supplied for the File Output Plugin: <outfilepath>")
        else:
            return FileOutPlugin(filepath)