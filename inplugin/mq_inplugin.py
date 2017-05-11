from inplugin import InPlugin
import time
import pika
import json
from common.funits import Fvalue


class MQInPlugin(InPlugin):
    """
    It inherits from InPlugin and it overrides the run method to start the start_consuming procedure
    instead of implementing the while True loop of other plugins
    """
    def __init__(self, coll_period, mq_machine, routing_key):
        """
        A RabbitMQ in plugin that is going to consume messages from a queue t
        :param coll_period: collect period. Ignored since there won't be a collect method and run will be overrided
        :param mq_machine: this is the ip and port of the mq service we will use. It has the format IP:PORT
        :param routing_key: the routing key. It will be the name of the machine is going to consume the data
        """
        InPlugin.__init__(self, coll_period)
        host_and_port = mq_machine.split(":")
        self.mq_host = host_and_port[0]
        if len(host_and_port) > 1:
            self.mq_port = int(host_and_port[1])
        else:
            self.mq_port = None # default port is 5672
        self.routing_key = routing_key

    def run(self):
        """
        This function represents the thread that is going to run in parallel listening to the queue
        :rtype: object
        """

        def callback(ch, method, properties, body):
            json_body = json.loads(body)
            self.buffer.append(Fvalue.fromdict(json_body))

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.mq_host,port=self.mq_port))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.mq_host + '_exchange', type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.mq_host + '_exchange',
                           queue=queue_name,
                           routing_key=self.routing_key)
        channel.basic_consume(callback,queue=queue_name,no_ack=True)
        channel.start_consuming()
