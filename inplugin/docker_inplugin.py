from inplugin import InPlugin
from subprocess import check_output
from common import docker_metrics_refiner

class DockerInPlugin(InPlugin):
    def __init__(self, coll_period):
        """
        A plugin that connects to the Docker socket and retrieves stats about the running containers. Because
        connecting each time to the socket it's expensive we will start one thread for each of the containers 
        :param coll_period: 
        """
        InPlugin.__init__(self, coll_period)

    def collect(self):
        # give me a json with a set of stats for all the docker containers in this host
        stats = docker_metrics_refiner.docker_stats()
