from outplugin import OutPlugin
import pika
import json
from time import sleep


class MQOutPlugin(OutPlugin):
    def __init__(self, mq_machine, routing_key):
        """
        A RabbitMQ out plugin that pushes messages to an exchange with name 'mq_machine' + '_exchange'
        and routing key routing_key so it will be delivered to the right consumer
        :param mq_machine: this is the ip and port of the mq service we will use. It has the format IP:PORT
        :param routing_key: this is the machine that will consume the data
        """
        OutPlugin.__init__(self)
        host_and_port = mq_machine.split(":")
        self.mq_host = host_and_port[0]
        if len(host_and_port) > 1:
            self.mq_port = int(host_and_port[1])
        else:
            self.mq_port = None
        self.routing_key = routing_key
        sleep(5) # We introduce a slight delay to let the RabbitMQ container to accept connections
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.mq_host,port=self.mq_port))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange= self.mq_host + '_exchange',exchange_type='direct')

    def push(self,refineddata):
        if refineddata: # only push data if we have some
            for fvalue in refineddata:
                self.channel.basic_publish(exchange= self.mq_host + '_exchange',
                                           routing_key=self.routing_key,
                                           body=json.dumps(fvalue.__dict__))
                print "Publishing the following values to machine {0} with routing key {1}"\
                    .format(self.mq_host,self.routing_key)
                print fvalue.__dict__.__str__()

