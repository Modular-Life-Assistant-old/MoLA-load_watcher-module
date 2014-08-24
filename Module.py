from core import Log
from core import EventManager

import subprocess
import time

class Module:
    def __init__(self):
        self.__max_average = int(subprocess.check_output([
            'grep',
            '-c',
            '^processor',
            '/proc/cpuinfo'
        ]))

    def thread_check(self):
        while True:
            average = float(subprocess.check_output([
                'cat',
                '/proc/loadavg'
            ]).split()[0])

            if average > self.__max_average:
                message = 'Average at %f (max: %d)' % (average, self.__max_average)
                Log.warning(message)
                EventManager.trigger(
                    'perf_alert',
                    message=message,
                )

            time.sleep(60)

