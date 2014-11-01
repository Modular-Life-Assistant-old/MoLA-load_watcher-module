from core import Log

from circuits import Component, Event, Timer
import subprocess
import time


class load_alert(Event):
    """ Event raised when load is to high
    """
    def __init__(self, load, load_max, timestamp):
        super(load_alert, self).__init__(load, load_max, timestamp)


class Module(Component):
    channel = 'load_avg'
    delay = 60
    max_avg = 0

    def get_load_avg(self):
        avg_cmd = ['cat', '/proc/loadavg']
        output = subprocess.check_output(avg_cmd)
        avg = float(output.split()[0])

        if avg >= self.max_avg:
            Log.warning('Average at %f (max: %d)' % (avg, self.max_avg))
            self.fire(load_alert(avg, self.max_avg, time.time()))

    def started(self, component):
        process_cmd = ['grep', '-c', '^processor', '/proc/cpuinfo']
        cpu_count = subprocess.check_output(process_cmd)
        self.max_avg = int(cpu_count)
        load_avg_evt = Event.create('get_load_avg')
        Timer(self.delay, load_avg_evt, self.channel, persist=True).register(self)

