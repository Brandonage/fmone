from outplugin import OutPlugin
import pika


class MQOutPlugin(OutPlugin):
    def __init__(self, mq_machine, routing_key):
        """
        A RabbitMQ out plugin that pushes messages to an exchange with name 'mq_machine' + '_exchange'
        and routing key routing_key so it will be delivered to the right consumer
        :param mq_machine: this is the ip of the machine where the RabbitMQ service resides
        :param routing_key: this is the machine that will consume the data
        """
        OutPlugin.__init__(self)
        self.mq_machine = mq_machine
        self.routing_key = routing_key
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.mq_machine))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange= self.mq_machine + '_exchange',type = 'direct')

    def push(self,refineddata):
        if refineddata is not None: # only push data if we have some
            for fvalue in refineddata:
                self.channel.basic_publish(exchange= self.mq_machine + '_exchange',
                                           routing_key=self.routing_key,
                                           body=fvalue.__dict__.__str__())
                print "Publishing the following values to machine {0} with routing key {1}"\
                    .format(self.mq_machine,self.routing_key)
                print fvalue.__dict__.__str__()

