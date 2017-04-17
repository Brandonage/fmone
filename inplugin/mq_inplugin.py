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
        :param mq_machine: this is the ip of the mq service we will use
        :param routing_key: the routing key. It will be the name of the machine is going to consume the data
        """
        InPlugin.__init__(self, coll_period)
        self.mq_machine = mq_machine
        self.routing_key = routing_key

    def run(self):
        """
        This function represents the thread that is going to run in parallel listening to the queue
        :rtype: object
        """

        def callback(ch, method, properties, body):
            json_body = json.loads(body)
            self.buffer.append(Fvalue.fromdict(json_body))

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.mq_machine))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.mq_machine + '_exchange', type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.mq_machine + '_exchange',
                           queue=queue_name,
                           routing_key=self.routing_key)
        channel.basic_consume(callback,queue=queue_name,no_ack=True)
        channel.start_consuming()
