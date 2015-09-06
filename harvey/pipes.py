from gevent import Greenlet, sleep
from harvey.utils import timeit

import logging
log = logging.getLogger(__name__)


class Worker(Greenlet):

    def __init__(self, frontier, queue):
        Greenlet.__init__(self)
        self.frontier = frontier
        self.queue = queue

    def do(self):
        raise NotImplementedError

    def _run(self):
        while True:
            self.do()


class URLFeeder(Worker):

    def do(self):
        url = timeit(self.frontier.pop, 'feeder')
        if not url:
            sleep(5)
        else:
            self.queue.put(url)


class ResultProcessor(Worker):

    def do(self):
        origin, urls = self.queue.get()
        timeit(self.frontier.add, origin, origin, urls)
