import json
import logging
import re
import sched
import subprocess
from datetime import timedelta

import psutil
import time
from urllib import request, parse

_STR_COMP = 'Computer'
_STR_GPU_UTIL = 'GPU util'
_STR_CPU_UTIL = 'CPU util'
_STR_TIME = 'Time'
_STR_INTV = 'Interval'
_STR_DEVICE = 'Device name'
_STR_HAS_GPU = 'GPU Present'

UNITS = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}


def convert_to_seconds(s):
    """Convert time string to seconds. Source:
    https://stackoverflow.com/questions/3096860/convert-time-string-expressed-as-numbermhdsw-to-seconds-in-python
    """
    return int(timedelta(**{
        UNITS.get(m.group('unit').lower(), 'seconds'): float(m.group('val'))
        for m in re.finditer(r'(?P<val>\d+(\.\d+)?)(?P<unit>[smhdw]?)', s, flags=re.I)
    }).total_seconds())


def get_usage(config):
    # Get CPU usage
    cpu_load = psutil.getloadavg()[0]  # average CPU Load (in cores) for last 1 min
    cpu_load_percent = cpu_load / psutil.cpu_count() * 100

    # Get GPU usage
    gpu_load_percent = 0.0
    if config[_STR_COMP][_STR_HAS_GPU]:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.used,memory.total,utilization.gpu',
                                  '--format=csv,noheader,nounits'], capture_output=True)
        result_data = result.stdout.decode().strip().split('\n')
        gpu_load_percent_all = [float(line.strip()[-1]) for line in result_data]
        gpu_load_percent = sum(gpu_load_percent_all) / len(gpu_load_percent_all)

    return cpu_load_percent, gpu_load_percent


def check_idle(config, scheduler, metadata):

    # Get usage
    cpu_load, gpu_load = get_usage(config)

    idling = (cpu_load < config[_STR_COMP][_STR_CPU_UTIL] and gpu_load < config[_STR_COMP][_STR_GPU_UTIL])

    if idling:
        if not metadata['notified']:
            if metadata['idle_since'] is None:
                # First idling instance: Take note of when it started
                metadata['idle_since'] = time.time()
            else:
                t_elapsed = time.time() - metadata['idle_since']
                if t_elapsed >= config[_STR_COMP][_STR_TIME]:
                    notify(config, (cpu_load, gpu_load))
                    metadata['notified'] = True

    else:
        metadata['idle_since'] = None
        metadata['notified'] = False

    print('CPU: {}%, GPU: {}%'.format(cpu_load, gpu_load))

    scheduler.enter(config[_STR_COMP][_STR_INTV], 1, check_idle, (config, scheduler, metadata))


def notify(config, cpu_gpu_load):
    data = parse.urlencode({
        'key': config['key'],
        'title': '{} idle'.format(config[_STR_COMP][_STR_DEVICE]),
        'msg': 'Current load: {:.1f} (CPU), {:.1f} (GPU)'.format(cpu_gpu_load[0], cpu_gpu_load[1]),
        'event': 'event'
    }).encode()
    req = request.Request("https://api.simplepush.io/send", data=data)
    request.urlopen(req)
    print('Notify!')


def main(config):
    scheduler = sched.scheduler(time.time, time.sleep)
    metadata = {'idle_since': None, 'notified': False}

    scheduler.enter(config[_STR_COMP][_STR_INTV], 1, check_idle, (config, scheduler, metadata))
    scheduler.run()


if __name__ == '__main__':
    # Loads config
    with open('config.json') as fid:
        cfg = json.load(fid)
        cfg[_STR_COMP][_STR_CPU_UTIL] = float(cfg[_STR_COMP][_STR_CPU_UTIL])
        cfg[_STR_COMP][_STR_GPU_UTIL] = float(cfg[_STR_COMP][_STR_GPU_UTIL])
        cfg[_STR_COMP][_STR_INTV] = convert_to_seconds(cfg[_STR_COMP][_STR_INTV])
        cfg[_STR_COMP][_STR_TIME] = convert_to_seconds(cfg[_STR_COMP][_STR_TIME])

    main(cfg)
