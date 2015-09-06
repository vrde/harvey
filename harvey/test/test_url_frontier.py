from time import time as _time
from collections import Counter

from harvey.frontier import URLFrontier
import pytest


def test_pop_returns_none_if_no_more_urls_are_available(monkeypatch):
    u = URLFrontier(Counter(), ignore_url=None)
    url_1 = 'http://www.example.org/'
    url_2 = 'http://www.example.org/index.html'
    elements = set()

    monkeypatch.setattr('time.time', lambda: 0)
    waittime = u.add(url_1)
    print(waittime)

    monkeypatch.setattr('time.time', lambda: waittime)
    waittime = u.add(url_2)
    print(waittime)

    elements.add(u.pop())
    assert len(elements) == 1
    assert u.pop() == None

    # we need another `pop` 10s later to remove the host from the list
    monkeypatch.setattr('time.time', lambda: waittime + 10)
    elements.add(u.pop())
    assert len(elements) == 2
    assert elements == set([url_1, url_2])
    monkeypatch.setattr('time.time', lambda: waittime + 20)
    assert u.pop() == None

    # heap should be empty as well
    assert len(u.hosts) == 0
    assert len(u.hosts.keys) == 0
    assert len(u.hosts.values) == 0

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

    # assert u.pop() == url_2
    # assert u.pop() == url_1
    # assert u.pop() == url_3


def test_adding_an_existing_url_to_frontier_doesnt_work():
    u = URLFrontier(Counter(), ignore_url=None)
    origin_1 = 'https://en.wikipedia.org/wiki/Whatever'
    url_1 = 'https://www.example.org/index.html'

    u.add(origin_1, url_1)
    u.add(origin_1, url_1)

    assert len(u.urls) == 1


def test_popping_a_url_disable_the_host_for_a_while(monkeypatch):
    u = URLFrontier(Counter(), ignore_url=None)
    origin_1 = 'https://en.wikipedia.org/wiki/Whatever'
    url_1 = 'https://en.wikipedia.org/wiki/Meh'
    url_2 = 'https://en.wikipedia.org/wiki/Interesting_(sarcasm)'
    url_3 = 'https://en.wikipedia.org/wiki/Foo'
    elements = set()

    monkeypatch.setattr('time.time', lambda: 0)
    waittime = u.add(origin_1, set([url_1, url_2, url_3]))
    # pytest.set_trace()
    assert u.pop() == None

    monkeypatch.setattr('time.time', lambda: waittime)
    elements.add(u.pop())
    assert u.pop() == None

    monkeypatch.setattr('time.time', lambda: waittime + 10)
    elements.add(u.pop())
    assert u.pop() == None

    monkeypatch.setattr('time.time', lambda: waittime + 20)
    elements.add(u.pop())
    assert u.pop() == None

    assert elements == set([url_1, url_2, url_3])


def test_adding_urls_at_the_same_time_does_not_fuckup_the_frontier(monkeypatch):
    pass
