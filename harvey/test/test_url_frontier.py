from harvey.frontier import URLFrontier
from collections import Counter


def test_pop_returns_none_if_no_more_urls_are_available():
    u = URLFrontier(Counter(), ignore_url=None)
    url = 'http://www.example.org/'
    u.add(url)
    assert u.pop() == url
    assert u.pop() == None

    # heap should be empty as well
    assert len(u.hosts.elements) == 0
    assert len(u.hosts.heap) == 0

    # and the bucket should have been removed
    assert len(u.buckets) == 0


def test_adding_url_to_frontier_adds_it_to_the_priority_queue(monkeypatch):
    u = URLFrontier(Counter(), ignore_url=None)
    origin_1 = 'https://en.wikipedia.org/wiki/Whatever'
    url_1 = 'https://www.example.org/index.html'

    # time is not important because new domains will be added to the
    # heap with priority zero
    # monkeypatch.setattr('time.time', lambda: 100)
    u.add(origin_1, url_1)

    origin_2 = 'https://www.torproject.org/i-luv-nsa.html'
    url_2 = 'https://internetdefenseleague.org/'

    # time is not important because new domains will be added to the
    # heap with priority zero
    # monkeypatch.setattr('time.time', lambda: 200)
    u.add(origin_2, url_2)

    # url_3 = 'https://internetdefenseleague.org/whatever.html'
    u.add(origin_2, url_2)

    assert u.pop() == url_2
    assert u.pop() == url_1
    # assert u.pop() == url_3


def test_adding_an_existing_url_to_frontier_doesnt_work():
    u = URLFrontier(Counter(), ignore_url=None)
    origin_1 = 'https://en.wikipedia.org/wiki/Whatever'
    url_1 = 'https://www.example.org/index.html'

    u.add(origin_1, url_1)
    u.add(origin_1, url_1)

    assert len(u.urls) == 1
