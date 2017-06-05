"""
This is a module to extract a curated set of docker stats out of the dict from the stats() method of dockerpy. 
We developed it inside the common package and decoupled from the Inplugin so it could be reusable in other projects
"""

import docker
import pprint
from datetime import datetime
from time import sleep

def get_summary_dict(dict):
    """
    It creates a summary dict from the dictionary returned by the stats method in the Docker SDK
    :rtype: dict
    :param dict: a dict that comes from calling container.stats()
    """
    usr_cpu_time = dict.get('cpu_stats', {}).get('cpu_usage', {}).get('usage_in_usermode', 0) # we need to calculate percents from this
    wait_cpu_time = dict.get('cpu_stats', {}).get('cpu_usage', {}).get('usage_in_kernelmode', 0)
    cpu_total_time = dict.get('cpu_stats', {}).get('cpu_usage', {}).get('total_usage', 0)
    overall_cpu_time = dict.get('cpu_stats', {}).get('system_cpu_usage', 0)
    num_procs = dict.get('num_procs',0)
    # If the container runs on host mode there won't be network metrics. We use the safe method get
    rec_bytes = dict.get('networks',{}).get('eth0',{}).get('rx_bytes',0)
    sent_bytes = dict.get('networks',{}).get('eth0',{}).get('tx_bytes',0)
    rec_errors = dict.get('networks',{}).get('eth0',{}).get('rx_errors',0)
    sent_errors = dict.get('networks',{}).get('eth0',{}).get('tx_errors',0)
    rec_dropped = dict.get('networks',{}).get('eth0',{}).get('rx_dropped',0)
    sent_dropped = dict.get('networks',{}).get('eth0',{}).get('tx_dropped',0)
    mem_limit =  dict.get('memory_stats',{}).get('limit',0)
    mem_usage = dict.get('memory_stats',{}).get('usage',0)
    max_usage = dict.get('memory_stats',{}).get('max_usage',0)
    stack_mem = dict.get('memory_stats',{}).get('stats',{}).get('total_rss',0)
    cache_mem = dict.get('memory_stats',{}).get('stats',{}).get('total_cache',0)
    major_page_fault = dict.get('memory_stats',{}).get('stats',{}).get('total_pgmajfault',0)
    page_fault = dict.get('memory_stats',{}).get('stats',{}).get('total_pgfault',0)
    try:
        write_bytes = dict['blkio_stats']['io_service_bytes_recursive'][1]['value']
        read_bytes = dict['blkio_stats']['io_service_bytes_recursive'][0]['value']
    except IndexError:
        write_bytes = 0
        read_bytes = 0
    summary_dict = {
        'usr_cpu_time': usr_cpu_time,
        'wait_cpu_time': wait_cpu_time,
        'cpu_total_time': cpu_total_time,
        'overall_cpu_time': overall_cpu_time,
        'num_procs': num_procs,
        'rec_bytes': rec_bytes,
        'sent_bytes': sent_bytes,
        'rec_errors': rec_errors,
        'sent_errors': sent_errors,
        'rec_dropped': rec_dropped,
        'sent_dropped': sent_dropped,
        'mem_limit': mem_limit,
        'mem_usage': mem_usage,
        'max_usage': max_usage,
        'stack_mem': stack_mem,
        'cache_mem': cache_mem,
        'major_page_fault': major_page_fault,
        'page_fault': page_fault,
        'write_bytes': write_bytes,
        'read_bytes': read_bytes
    }
    return summary_dict

def calculate_cpu_percentage(dict,prev_dict):
    cpu_system = dict['overall_cpu_time']
    cpu_system_prev = prev_dict['overall_cpu_time']
    cpu_container = dict['cpu_total_time']
    cpu_container_prev = prev_dict['cpu_total_time']
    cpu_usr_container = dict['usr_cpu_time']
    cpu_usr_container_prev = prev_dict['usr_cpu_time']
    cpu_wait_container = dict['wait_cpu_time']
    cpu_wait_container_prev = prev_dict['wait_cpu_time']
    cpu_delta = cpu_container - cpu_container_prev
    system_delta = cpu_system - cpu_system_prev
    cpu_wait_delta = cpu_wait_container - cpu_wait_container_prev
    cpu_usr_delta = cpu_usr_container - cpu_usr_container_prev
    cpu_percent = 0
    cpu_wait_percent = 0
    cpu_usr_percent = 0
    if (system_delta > 0) and (cpu_delta > 0):
        cpu_percent = float(cpu_delta)/float(system_delta) * 100
        cpu_wait_percent = float(cpu_wait_delta)/float(system_delta) * 100
        cpu_usr_percent = float(cpu_usr_delta)/float(system_delta) * 100
    return cpu_percent, cpu_wait_percent, cpu_usr_percent

def refine_docker_stats(dict, prev_dict): # TODO: CHANGE THE UNITS OF MEASUREMENT
    """
    Returns a dictionary with a set of curated metrics out of two dicts: The actual stats metrics and the stats metrics
    from the previous iteration
    :param dict: The dict just collected by the stats method 
    :param prev_dict: The previous dict of the stream. We use it to calculate CPU % and some other changes 
    """
    summary = get_summary_dict(dict)
    prev_summary = get_summary_dict(prev_dict)
    cpu_percent, cpu_wait_percent, cpu_usr_percent = calculate_cpu_percentage(summary,prev_summary)
    mem_percent_used = float(summary['mem_usage'])/float(summary['mem_limit'])
    # we add the new calculated values
    summary['cpu_percent'] = cpu_percent
    summary['cpu_wait_percent'] = cpu_wait_percent
    summary['cpu_usr_percent'] = cpu_usr_percent
    summary['mem_percent_used'] = mem_percent_used
    return summary


if __name__ == '__main__':
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    c= client.containers.list()[0] ## OJO. LA LISTA PUEDE ESTAR VACIA
    stream = c.stats(decode=True)
    prev_chunk = None # We start with an empty previous chunk
    for chunk in stream:
        if prev_chunk is None: # if we are starting to retrieve chunks then the previous chunk is the actual one
            prev_chunk = chunk
        # we proceed to check the year this chunk was read
        datetime_object = datetime.strptime(chunk['read'][0:10],'%Y-%m-%d')
        # we need to know if the container is still running.
        # If it's not then we just exit since we don't want to monitor it anymore
        if datetime_object.year == 1: # '{"read":"0001-01-01T00:00:00Z","preread":"0001-01-01T00:00:00Z" this are the values when a container is not running
            exit()
        refined_chunk = refine_docker_stats(chunk,prev_chunk)
        pprint.pprint(refined_chunk)
        sleep(5)


