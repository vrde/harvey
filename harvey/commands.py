from urllib.parse import urlparse

import gevent.queue
from gevent_utils import Watch, Group
from collections import Counter

from harvey import settings
from harvey.crawler import Crawler
from harvey.frontier import URLFrontier
from harvey.pipes import URLFeeder, ResultProcessor


def ignore_url(url):
    hostname = urlparse(url).hostname
    return not hostname.endswith('.onion')


def run_crawler(arguments):
    stats = Counter()
    w = Watch(stats)
    w.start()
    
    q_urls = gevent.queue.Queue(settings.REQUEST_CONCURRENCY * 10)
    q_results = gevent.queue.Queue(settings.REQUEST_CONCURRENCY * 10)
    # frontier = URLFrontier(stats, ignore_url=ignore_url)
    frontier = URLFrontier(stats)
    crawlers = Group(settings.REQUEST_CONCURRENCY, Crawler, args=(q_urls, q_results, stats))

    url_feeder = URLFeeder(frontier, q_urls)
    result_processor = ResultProcessor(frontier, q_results)

    # frontier.add('http://kpvz7kpmcmne52qf.onion/wiki/index.php/Main_Page')
    # frontier.add('http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page')
    frontier.add('https://en.wikipedia.org/')

    url_feeder.start()
    result_processor.start()

    return crawlers


def run(arguments):
    t = None

    if arguments.get('crawl'):
        t = run_crawler(arguments)

    if arguments.get('config'):
        from pprint import pprint
        pprint({k: v for k, v in settings.__dict__.iteritems()
                if not k.startswith('_')})

    if t is not None:
        t.start()
        t.join()
