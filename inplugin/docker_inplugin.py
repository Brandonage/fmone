from inplugin import InPlugin
from common import docker_metrics_refiner
import docker
from time import sleep, time
from threading import Thread
from common.funits import Fvalue
import socket


class StatsCollector(Thread):
    def __init__(self,container,buffer,coll_period):
        """
        This is a worker thread that will collect stats for a given container and publish it to the buffer of the 
        InPlugin every coll_period seconds
        :param container: the container to monitor
        :param buffer: the buffer of the InPlugin
        :param coll_period: collect stats every coll_period seconds
        """
        Thread.__init__(self)
        self.container = container
        self.buffer = buffer
        self.coll_period = coll_period
        self.stopper = False

    def stop(self):
        """
        Tells the StatsCollector to finish
        """
        self.stopper = True

    def stopped(self):
        return self.stopper

    def run(self):
        stream = self.container.stats(decode=True)
        prev_chunk = None
        for chunk in stream:
            if prev_chunk is None:  # if we are starting to retrieve chunks then the previous chunk is the actual one
                prev_chunk = chunk
            # we proceed to check the year this chunk was read
            # datetime_object = datetime.strptime(chunk['read'][0:10], '%Y-%m-%d')
            # # we need to know if the container is still running.
            # # If it's not then we just exit since we don't want to monitor it anymore
            # if datetime_object.year == 1:  # '{"read":"0001-01-01T00:00:00Z","preread":"0001-01-01T00:00:00Z" this are the values when a container is not running
            #     return
            if self.stopper: # this is the condition for the worker to stop
                break
            refined_chunk = docker_metrics_refiner.refine_docker_stats(chunk, prev_chunk)
            for name, value in refined_chunk.iteritems():
                value = Fvalue(fmetric="docker_" + name,
                               fhost=socket.gethostname(),
                               fvalue=value,
                               funit='todo', # TODO: Include the units
                               ftime=int(round(time() * 1000)),
                               finfo=self.container.image.tags[0] # we add the container image name to identify the software
                               )
                self.buffer.append(value)
            print len(self.buffer)
            sleep(self.coll_period)


class DockerInPlugin(InPlugin):
    def __init__(self, coll_period):
        """
        A plugin that connects to the Docker socket and retrieves stats about the running containers. Because
        connecting each time to the socket it's expensive we will start one thread for each of the containers 
        :param coll_period: Even if we override the run method to manage the streams of the different workers, we can
        use this parameter to determine how often we want to push the data to the buffer
        """
        InPlugin.__init__(self, coll_period)

    def run(self):
        # give me a json with a set of stats for all the docker containers in this host
        """
        We override this method since we are not going to call a collect method every coll_period seconds. Instead
        we are going to manage a set of worker threads inside this thread that will listen for the docker socket
        to send them stats 
        """
        client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        containers_registered = {}
        while True:
            containers = client.containers.list()
            for c in containers:
                if c.short_id not in containers_registered: # if the inplugin didn't have an account of this container
                    # we start a new collector thread for that container that will add values to the buffer
                    stats_collector = StatsCollector(container=c,buffer=self.buffer,coll_period=self.coll_period)
                    containers_registered[c.short_id] = stats_collector # add it to the register of Inpuglin
                    stats_collector.start()
            # we need to check which containers of the running containers dictionary doesn't exist anymore. We use sets
            set_cont_running = set([c.short_id for c in containers])
            set_cont_registered = set(containers_registered.keys())
            diff = list(set_cont_running.symmetric_difference(set_cont_registered))
            for key in diff: # for each of the containers in the difference set
                containers_registered[key].stop() # stop the worker thread
            sleep(3) # I sleep three seconds before refreshing the list of containers

if __name__ == '__main__':
    plugin = DockerInPlugin(2)
    plugin.run()



