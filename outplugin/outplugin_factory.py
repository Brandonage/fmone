# A factory to create outplugins
from file_outplugin import FileOutPlugin
from mq_outplugin import MQOutPlugin
from console_outplugin import ConsoleOutPlugin
from mongo_outplugin import MongoOutPlugin
from kafka_outplugin import KafkaOutPlugin


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
            raise ValueError("Wrong parameters supplied for the MQ Out Plugin: <mq_machine, routing_key>")
        return MQOutPlugin(mq_machine, routing_key)
    if plugin_type=="console":
        return ConsoleOutPlugin()
    if plugin_type=="mongodb":
        mongo_machine = args.get("mongo_machine_out")
        mongo_collection = args.get("mongo_collection_out")
        if (not isinstance(mongo_machine,str) or not isinstance(mongo_collection,str)):
            raise ValueError("Wrong parameters supplied for the MongoDB Out Plugin: <mongo_machine, mongo_collection")
        return MongoOutPlugin(mongo_machine,mongo_collection)
    if plugin_type=="kafka":
        bootstrap_server = args.get("kafka_bootstrap_out")
        topic = args.get("kafka_topic_out")
        if (not isinstance(bootstrap_server,str) or not isinstance(topic,str)):
            raise ValueError("Wrong parameters supplied for the Kafka Out Plugin: <kafka_bootstrap, topic>")
        return KafkaOutPlugin(bootstrap_server,topic)
