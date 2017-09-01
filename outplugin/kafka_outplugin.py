from outplugin import OutPlugin
from kafka import KafkaProducer
import json


class KafkaOutPlugin(OutPlugin):
    def __init__(self, bootstrap_server, topic):
        """
        A Kafka Outplugin that is going to publish messages to a Kafka cluster.
        :param bootstrap_broker: this is the bootstrap server that is going to connect the client to the cluster
        :param topic: the topic we want to publish to.
        """
        OutPlugin.__init__(self)
        self.bootstrap = bootstrap_server
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_server],
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'))

    def push(self,refineddata):
        if refineddata: # only push data if we have some
            for fvalue in refineddata:
                self.producer.send(topic=self.topic,value=fvalue.__dict__)
                print "Publishing the following values to machine {0} and to topic {1}"\
                    .format(self.bootstrap,self.topic)
                print fvalue.__dict__.__str__()

