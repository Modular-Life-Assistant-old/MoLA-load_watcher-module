from core import Log

from circuits import Component, Event, Timer
import os
import time


class load_alert(Event):
    """ Event raised when load is to high
    """
    def __init__(self, load, load_max, timestamp):
        super().__init__(load, load_max, timestamp)


class Module(Component):
    channel = 'load_avg'
    delay = 60
    max_avg = 0

    def get_load_avg(self):
        avg = os.getloadavg()[0]

        if avg >= self.max_avg:
            Log.warning('Average at %f (max: %d)' % (avg, self.max_avg))
            self.fire(load_alert(avg, self.max_avg, time.time()))

    def started(self, c):
        self.max_avg = os.cpu_count()
        load_avg_evt = Event.create('get_load_avg')
        Timer(self.delay, load_avg_evt, self.channel, persist=True).register(self)
