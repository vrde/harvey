from gevent import Greenlet
import requesocks
import lxml.html
from urlparse import urljoin
import urltools

from harvey import settings

import logging
log = logging.getLogger(__name__)


class Crawler(Greenlet):

    def __init__(self, q_urls, q_results, stats):
        Greenlet.__init__(self)
        self.q_urls = q_urls
        self.q_results = q_results
        self.stats = stats

    def _run(self):
        while True:
            url = self.q_urls.get()
            log.debug(u'Got new url: {}'.format(url))
            self.stats['q_urls'] = self.q_urls.qsize()
            self.stats['q_results'] = self.q_results.qsize()
            self.stats['waiting for response'] += 1

            try:
                r = self.get(url)
                urls = self.extract_urls(r)
                self.q_results.put((r.url, urls))
            except TypeError:
                pass
            except:
                log.exception(u'Exception while crawling {}'.format(url))
            self.stats['waiting for response'] -= 1

    def get(self, url):
        session = requesocks.session()
        session.proxies = settings.PROXIES
        r = session.get(url)
        return r

    def extract_urls(self, r):
        urls = set()
        tree = lxml.html.fromstring(r.text)

        for element, attribute, link, pos in tree.iterlinks():
            url = urltools.normalize(urljoin(r.url, link))
            urls.add(url)

        # self.stats['urls'] += len(urls)
        self.stats['processed'] += 1

        return urls
