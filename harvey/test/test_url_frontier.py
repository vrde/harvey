from harvey.frontier import URLFrontier


def test_adding_url_to_frontier_adds_it_to_the_priority_queue(monkeypatch):
    monkeypatch.setattr('time.time', lambda: 100)
    u = URLFrontier()
    origin_1 = 'https://en.wikipedia.org/wiki/Whatever'
    url_1 = 'https://www.example.org/index.html'

    u.add(origin_1, url_1)

    assert len(u.urls) == 1
    assert url_1 in u.urls
    assert len(u.buckets['www.example.org']) == 1
    assert (0, 'www.example.org') in u.hosts_heap
    assert (110, 'en.wikipedia.org') in u.hosts_heap

    origin_2 = 'https://www.torproject.org/i-luv-nsa.html'
    url_2 = 'https://internetdefenseleague.org/'

    u.add(origin_2, url_2)

    assert len(u.urls) == 2
    assert url_2 in u.urls
    assert (0, 'internetdefenseleague.org') in u.hosts_heap
    assert (110, 'www.torproject.org') in u.hosts_heap


def test_adding_an_existing_url_to_frontier_doesnt_work():
    u = URLFrontier()
    origin_1 = 'https://en.wikipedia.org/wiki/Whatever'
    url_1 = 'https://www.example.org/index.html'

    u.add(origin_1, url_1)
    u.add(origin_1, url_1)

    assert len(u.urls) == 1
