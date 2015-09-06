"""Harvey

Usage:
  harvey crawl [--multicore]
  harvey config
  harvey (-h | --help)
  harvey --version

Options:
  --multicore     Spawn subprocesses.
  -h --help       Show this screen.
  --version       Show version.
  --logfile=FILE  Override the default log file (harvey.log)
"""

import gevent.monkey

gevent.monkey.patch_all()


from harvey import settings
from harvey import utils

# And we need to init the logging system BEFORE some module
# tries to use it
import logging.config
import logging
from docopt import docopt
from multiprocessing import cpu_count
from subprocess import Popen
import signal
import sys
import time


def run(arguments):
    from harvey import commands
    commands.run(arguments)


def configure_logging(arguments):
    logfile = arguments.get('--logfile')

    if logfile:
        override_logfile = {'handlers': {'file': {'filename': logfile}}}
        settings.LOGGING = utils.update(settings.LOGGING, override_logfile)

    logging.config.dictConfig(settings.LOGGING)


def main():
    def killall(signal, frame):
        print('Got signal {}, quitting'.format(signal))
        for proc in procs:
            proc.kill()
        sys.exit(0)

    signal.signal(signal.SIGTERM, killall)
    signal.signal(signal.SIGQUIT, killall)

    arguments = docopt(__doc__, version='harvey 0.0.1')
    procs = []
    if arguments['--multicore']:
        sys.argv.remove('--multicore')
        for i in range(cpu_count()):
            values = {
                'process_num': i + 1
            }
            custom_args = map(lambda x: x.format(**values), sys.argv)
            procs.append(Popen(custom_args))
            time.sleep(5)
        for proc in procs:
            proc.wait()

    else:
        configure_logging(arguments)
        run(arguments)


if __name__ == '__main__':
    main()
