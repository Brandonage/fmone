from outplugin import OutPlugin
from pymongo import MongoClient

class MongoOutPlugin(OutPlugin):
    def __init__(self,mongo_ip,collection_name):
        """
        A MongoOutPlugin that stores all the messages in a MongoDB
        :param mongo_ip contains an ip:port e.g 128.16.23.47:27017
        :param collection_name the name of the collection. Useful if we want to have a different
        collection for each fmone agent
        :type mongo_ip: str
        """
        OutPlugin.__init__(self)
        host_and_port = mongo_ip.split(":")
        self.mongo_host = host_and_port[0]
        if len(host_and_port) > 1:
            self.mongo_port = int(host_and_port[1])
        else:
            self.mongo_port = 27017 # the default mongo port
        self.client = MongoClient(self.mongo_host,self.mongo_port)
        self.db = self.client.fmone
        self.collection = self.db[collection_name]

    def push(self,refineddata):
        if refineddata: # only push data if we have some
            json_bulk = map(lambda x: x.__dict__, refineddata)
            result = self.collection.insert_many(json_bulk)
            print "Inserting into the MongoDB the following values: "
            print json_bulk
