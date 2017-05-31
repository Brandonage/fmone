"""
This is a module to extract a curated set of docker stats out of the dict from the stats() method of dockerpy. 
We developed it inside the common package and decoupled from the Inplugin so it could be reusable in other projects
"""

import docker
import pprint
from datetime import datetime

def get_summary_dict(dict):
    """
    It creates a summary dict from the dictionary returned by the stats method in the Docker SDK
    :rtype: dict
    :param dict: a dict that comes from calling container.stats()
    """
    usr_cpu_time = dict['cpu_stats']['cpu_usage']['usage_in_usermode'] # we need to calculate percents from this
    wait_cpu_time = dict['cpu_stats']['cpu_usage']['usage_in_kernelmode']
    cpu_total_time = dict['cpu_stats']['cpu_usage']['total_usage']
    overall_cpu_time = dict['cpu_stats']['system_cpu_usage']
    num_procs = dict['num_procs']
    rec_bytes = dict['networks']['eth0']['rx_bytes']
    sent_bytes = dict['networks']['eth0']['tx_bytes']
    rec_errors = dict['networks']['eth0']['rx_errors']
    sent_errors = dict['networks']['eth0']['tx_errors']
    rec_dropped = dict['networks']['eth0']['rx_dropped']
    sent_dropped = dict['networks']['eth0']['tx_dropped']
    mem_limit =  dict['memory_stats']['limit']
    mem_usage = dict['memory_stats']['usage']
    max_usage = dict['memory_stats']['max_usage']
    stack_mem = dict['memory_stats']['stats']['total_rss']
    cache_mem = dict['memory_stats']['stats']['total_cache']
    major_page_fault = dict['memory_stats']['stats']['total_pgmajfault']
    page_fault = dict['memory_stats']['stats']['total_pgfault']
    write_bytes = dict['blkio_stats']['io_service_bytes_recursive'][1]['value']
    read_bytes = dict['blkio_stats']['io_service_bytes_recursive'][0]['value']
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
    client = docker.from_env()
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


