# A factory to create outplugins
from file_outplugin import FileOutPlugin
from mq_outplugin import MQOutPlugin


def getoutplugin(plugin_type,**args):

    if plugin_type=="file":
        filepath = args.get("outfilepath")
        if not isinstance(filepath,str):
            raise ValueError("Wrong parameters supplied for the File Output Plugin: <outfilepath>")
        else:
            return FileOutPlugin(filepath)
    if plugin_type=="rabbitmq": # it needs mq_machine and routing_key as parameters
        mq_machine = args.get("mq_machine_out")
        routing_key = args.get("routing_key_out")
        if (not isinstance(mq_machine,str) or not isinstance(routing_key,str)):
            raise ValueError("Wrong parameters supplied for the MQ In Plugin: <mq_machine, routing_key>")
        return MQOutPlugin(mq_machine, routing_key)
