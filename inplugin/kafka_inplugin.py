from inplugin import InPlugin
from kafka import KafkaConsumer
import json
from common.funits import Fvalue


class KafkaInPlugin(InPlugin):
    def __init__(self, coll_period, bootstrap_server, topic):
        """
        A Kafka in plugin that is going to consume messages from a topic. The message group is always going to be the
        same as we want all the agents for a particular specific region topic to consume all the messages
        :param coll_period: Ignored since there won't be a collect method and run will be overriden. Same as RabbitMQ
        :param bootstrap_server: this is the IP:PORT of the kafka broker we will use to bootstrap.
        :param topic: the name of the topic where we are going to consume the messages from.
        """
        InPlugin.__init__(self, coll_period)
        self.bootstrap = bootstrap_server
        self.topic = topic
        self.producer = KafkaConsumer(self.topic,
                                      bootstrap_servers=[bootstrap_server],
                                      value_deserializer=lambda m: json.loads(m.decode('ascii')),
                                      group_id='fmone_group' ## A unique group for the topic server
                                      )

    def run(self):
        """
        This function represents the thread that is going to run in parallel listening to the queue
        :rtype: object
        """
        for message in self.producer:
            self.buffer.append(Fvalue.fromdict(message.value))

