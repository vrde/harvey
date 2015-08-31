"""The module is responsible for two main features of a crawler:
 - manage the URL frontier, that is basically a set of URL to crawl next;
 - do not open overlapping connections to a server.

To implement the first feature, a URLFrontier instance has a set called
``urls`` to keep track of all the URLs crawled so far. In future this will
be saved in a database or in a persistent Bloom Filter, such as `bloomd`_
or `pyreBloom`_.


Related to the implementation of the second feature the crawler, to be
a good internet citizen, **must not** hit servers too hard.
To achieve that, we need one **heap of domains** and as many
**URLs queues** as the number of domains we are crawling.
The **heap of domains** maps a domain to its **URLs bucket**.
The priority is given by the timestamp of the last time a URL from that
domain has been crawled.
When an instance of the crawler asks for a new URL to crawl, it calls the
``URLFrontier.pop`` method. The method pops a ``(domain, bucket)``
tuple from the **priority queue of domains** to get the next available
domain to crawl, then it uses the ``bucket`` object to pop a **URL** to
return to the crawler.

The complementary action is to **add** URLs to the URLFrontier.
After extracting the URLs from an HTML document, the crawler calls
``URLFrontier.add`` passing the domain (i.e. the domain where the
request was originated) and the URLs extracted.


.. _bloomd https://github.com/armon/bloomd
   _pyreBloom https://github.com/seomoz/pyreBloom

"""
from urlparse import urlparse
from collections import defaultdict
from operator import itemgetter
import time

from harvey import settings
from harvey.heap import InMemoryHeap
from harvey.sorted_collection import SortedKeyValue

import logging
log = logging.getLogger(__name__)


try:
    ignore_url = settings.IGNORE_URL_FUNC
except AttributeError:
    ignore_url = None


class URLFrontier(object):

    def __init__(self, stats, ignore_url=ignore_url):
        self.stats = stats
        self.ignore_url = ignore_url

        self.urls = set()
        self.buckets = defaultdict(set)
        self.hosts = InMemoryHeap()
        self.hosts_waitlist = SortedKeyValue(key=itemgetter(1),
                                             value=itemgetter(0))

    def get_waittime(self, domain):
        return int(time.time()) + 10

    def add(self, origin, urls=None):
        hostname = urlparse(origin).hostname
        waittime = self.get_waittime(hostname)

        if not urls:
            urls = set([origin])

        if not isinstance(urls, set):
            urls = set([urls])

        new_urls = urls - self.urls

        self.hosts.push(waittime, hostname)

        for url in new_urls:
            hostname = urlparse(url).hostname

            if self.ignore_url and self.ignore_url(url, hostname):
                continue

            self.buckets[hostname].add(url)
            if hostname not in self.hosts:
                self.hosts.push(0, hostname)

        log.debug('Found {} new urls'.format(len(new_urls)))
        self.urls.update(new_urls)
        self.stats['URLs frontier'] = len(self.urls)
        self.stats['hostnames'] = len(self.hosts)
        return waittime

    def eventually_add_host_to_heap(self):
        try:
            host = self.hosts_waitlist.find_le(time.time())
        except ValueError:
            pass
        else:
            self.hosts.push(*host)

    def pop(self):
        self.eventually_add_host_to_heap()
        url = None
        while url is None:
            try:
                hostname = self.hosts.pop()
            except IndexError:
                return

            try:
                url = self.buckets[hostname].pop()
            except KeyError:
                del self.buckets[hostname]
            else:
                self.hosts_waitlist.insert((self.get_waittime(hostname), hostname))

        return url
