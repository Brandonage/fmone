from inplugin import InPlugin
from subprocess import check_output
from common import docker_metrics

class DockerInPlugin(InPlugin):
    def __init__(self, coll_period):
        InPlugin.__init__(self, coll_period)

    def collect(self):
        output = check_output("docker ps --no-trunc | awk '{print $1 \"|\" $2}' | grep -v CONTAINER",shell=True)
        ps_and_name_tuples = map(lambda x: x.split("|"), output.split("\n")[:-1])
        for ps_name_tuple in ps_and_name_tuples:
            cputimes = docker_metrics.docker_stats() # give me the cpu stats for this ps number
