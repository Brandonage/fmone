# A factory to create inplugins

from cpu_inplugin import CpuInPlugin
from mq_inplugin import MQInPlugin
from host_inplugin import HostMetricsInPlugin
from docker_inplugin import DockerInPlugin
from kafka_inplugin import KafkaInPlugin

def getinplugin(plugin_type, coll_period, **args):
    if plugin_type=="cpu":
        return CpuInPlugin(coll_period)
    if plugin_type=="rabbitmq": # it needs parameters mq_machine and routing_key
        mq_machine = args.get("mq_machine_in")
        routing_key = args.get("routing_key_in")
        if (not isinstance(mq_machine,str) or not isinstance(routing_key,str)):
            raise ValueError("Wrong parameters supplied for the MQ In Plugin: <mq_machine, routing_key>")
        return MQInPlugin(coll_period,mq_machine,routing_key)
    if plugin_type=="host":
        return HostMetricsInPlugin(coll_period)
    if plugin_type=="docker":
        return DockerInPlugin(coll_period)
    if plugin_type=="kafka": # it needs parameters mq_machine and routing_key
        bootstrap_server = args.get("kafka_bootstrap_in")
        topic = args.get("kafka_topic_in")
        if (not isinstance(bootstrap_server,str) or not isinstance(topic,str)):
            raise ValueError("Wrong parameters supplied for the Kafka In Plugin: <kafka_bootstrap, topic>")
        return KafkaInPlugin(coll_period,bootstrap_server,topic)