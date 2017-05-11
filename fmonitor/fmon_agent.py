import sys
import os
sys.path.extend(["../../fmone"]) # For Docker. We set the PYTHONPATH two levels above to import the whole project.
from inplugin import inplugin_factory
from outplugin import outplugin_factory
from midplugin import midplugin_factory
import time
import argparse



class FMonAgent():
    def __init__(self,coll_period,push_period,inplugin,midplugin,outplugin,**args):
        """
        This is the agent monitor. It has a inplugin that collects monitored data, midplugin which filters this data
        and a outplugin that pushes this data to some sink.
        :param coll_period: we get data through inplugin.collect() every coll_period secs
        :param push_period: we push data to the sink every push_period. Only used here in this same class (FMonAgent.run())
        :param inplugin: An string that represents the inplugin created through a factory
        :param midplugin: An string that represents the midplugin created through a factory
        :param outplugin: An string that represents the outplugin created through a factory
        :param args: The arguments for each of the plugins. User needs to specify the names: param1=value1
        """
        try:
            self.inplugin = inplugin_factory.getinplugin(plugin_type=inplugin,coll_period=coll_period,**args)
            self.midplugin = midplugin_factory.getmidplugin(plugin_type=midplugin,)
            self.outplugin = outplugin_factory.getoutplugin(plugin_type=outplugin,**args)
            self.push_period = push_period

        except ValueError as err:
            print(err.args)

    def run(self):
        self.inplugin.start() # inplugin is going to run as a separate thread
        while True: # on the other hand we control the push process with the push_period parameter
            time1 = time.time()
            listofvalues = self.inplugin.pop() # pops the values of the buffer into a list of values
            refinedvalues = self.midplugin.refine(listofvalues) # refine the list of values
            self.outplugin.push(refineddata=refinedvalues) # push them out to the next fmon or backend
            time2 = time.time()
            timediff = time2-time1
            time.sleep(self.push_period - timediff)


def parse_fmone_args():
    """

    :return: A dict containing all the parameters parsed in the form of res.mongo_machine_out
    """
    home = os.environ['HOME']
    # These are the available options for the monitoring agent. Useful to print errors when using the script
    inplugins = ["cpu","rabbitmq"]
    midplugins = ["inout","average"]
    outplugins = ["file","rabbitmq","console","mongodb"]
    # We start to parse arguments
    parser = argparse.ArgumentParser(description="A monitoring util that can be customised with plugins")
    parser.add_argument('coll_period',help='Collect metrics every x_coll seconds',type=int,metavar='X_col',
                        default=5, nargs='?')
    parser.add_argument('push_period',help='Push metrics every x_push seconds',type=int,metavar='X_push',
                        default=5, nargs='?')
    parser.add_argument('inplugin',help='The type of in plugin we want to use',choices=inplugins)
    parser.add_argument('midplugin',help='The type of mid plugin we want to use',choices=midplugins)
    parser.add_argument('outplugin',help='The type of out plugin we want to use',choices=outplugins)
    parser.add_argument('--outfilepath',help='If using the file out plugin, which file to write to',
                        dest='outfilepath',default= home+ "/fmone.txt")
    parser.add_argument('--mq_machine_in',help='If using the rabbitMQ in plugin, the IP:Port of the rabbitMQ broker to communicate with',
                        dest='mq_machine_in')
    parser.add_argument('--routing_key_in',help='If using the rabbitMQ in plugin, the routing key we want to subscribe to',
                        dest='routing_key_in')
    parser.add_argument('--mq_machine_out',help='If using the rabbitMQ out plugin, the IP:Port of the rabbitMQ broker to communicate with',
                        dest='mq_machine_out')
    parser.add_argument('--routing_key_out',help='If using the rabbitMQ out plugin, the IP or name of the FMonAgent to which we want to send the messages',
                        dest='routing_key_out')
    parser.add_argument('--mongo_machine_out',help='If using the MongoDB out plugin, the IP or name of the FMonAgent to which we want to send the messages',
                        dest='mongo_machine_out')
    parser.add_argument('--mongo_collection_out',help='If using the MongoDB out plugin, the IP or name of the FMonAgent to which we want to send the messages',
                        dest='mongo_collection_out')
    res = parser.parse_args()
    return res


if __name__ == '__main__':
    args = parse_fmone_args()
    # fmonagent = FMonAgent(2,5,"cpu","inout","file",outfilepath= home + "/fmone.txt")
    # Some other examples
    # Agent that reads cpu and pushes to MQ as a message:
    # fmonagent = FMonAgent(2,5,"cpu","inout","rabbitmq",mq_machine_out="localhost",routing_key_out="mymaquina")
    # fmonagent = FMonAgent(2,5,"rabbitmq","inout","file",mq_machine_in="localhost",
    #                       routing_key_in="mymaquina",outfilepath= home + "/fmone.txt")
    fmonagent = FMonAgent(args.coll_period, args.push_period, args.inplugin, args.midplugin,args.outplugin,
                          outfilepath=args.outfilepath,
                          mq_machine_in=args.mq_machine_in,
                          routing_key_in=args.routing_key_in,
                          mq_machine_out=args.mq_machine_out,
                          routing_key_out=args.routing_key_out,
                          mongo_machine_out=args.mongo_machine_out,
                          mongo_collection_out=args.mongo_collection_out
                          )
    fmonagent.run()




