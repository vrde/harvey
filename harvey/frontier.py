"""The module is responsible for two main features of a crawler:
 - manage the URL frontier, that is basically a set of URL to crawl next;
 - do not open overlapping connections to a server.

To implement the first feature, a URLFrontier instance has a set called
``urls`` to keep track of all the URLs crawled so far. In future this will
be saved in a database or in a persistent Bloom Filter, such as `bloomd`_
or `pyreBloom`_.


Related to the implementation of the second feature the crawler, to be
a good internet citizen, **must not** hit servers too hard.
To achieve that, we need one **priority queue of domains** and as many
**URLs queues** as the number of domains we are crawling.
The **priority queue of domains** maps a domain to its **URLs bucket**.
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

C: hey frontier, I just visited a web page in **domain** and I found
   those 42 **urls**

F: Aww yissss! OK gimme a sec to:
 - remove from **urls** all the other URLs that we already have
 - add to the **priority queue of domains** the **domain** giving a
   priority value that is the current time (in seconds from 1/1/70) plus
   10 seconds (it's a way to put the domain back in the queue with a low
   priority)
 - for each **new URL**, put it in the right **URL bucket**, then extract
   the **domain** of the **URL** and update the **priority queue of domains**
   with maximum priority value (``0``)
 - add the **new URLs** to the set of URLs we already have

F: OK done, see you later
C: l8rz


.. _bloomd https://github.com/armon/bloomd
   _pyreBloom https://github.com/seomoz/pyreBloom

"""
import heapq
from urlparse import urlparse
from collections import defaultdict
import time
from harvey import settings

import logging
log = logging.getLogger(__name__)


try:
    ignore_url = settings.IGNORE_URL_FUNC
except AttributeError:
    ignore_url = None


class URLFrontier(object):

    def __init__(self, ignore_url=ignore_url):
        self.urls = set()
        self.buckets = defaultdict(set)
        self.hosts_heap = []
        self.hosts = set()
        self.ignore_url = ignore_url

    def add(self, origin, urls):
        domain = urlparse(origin).hostname

        if not isinstance(urls, set):
            urls = set([urls])

        new_urls = urls - self.urls

        heapq.heappush(self.hosts_heap, (int(time.time()) + 10, domain))
        self.hosts.add(domain)

        for url in new_urls:
            hostname = urlparse(url).hostname

            if self.ignore_url and self.ignore_url(url, hostname):
                continue

            self.buckets[hostname].add(url)
            if hostname not in self.hosts:
                heapq.heappush(self.hosts_heap, (0, hostname))
                self.hosts.add(hostname)

        log.debug('Found {} new urls'.format(len(new_urls)))
        self.urls.update(new_urls)

    def pop(self):
        try:
            _, hostname = heapq.heappop(self.hosts_heap)
            self.hosts.remove(hostname)
            url = self.buckets[hostname].pop()
            log.debug('Pop hostname {}'.format(hostname))
            return url
        except (KeyError, IndexError):
            return
