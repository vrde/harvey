from operator import itemgetter
from harvey.sorted_collection import SortedKeyValue


def test_insert():
    s = SortedKeyValue(itemgetter(1), itemgetter(0))
    s.insert((0, 'en.wikipedia.org'))

    assert s.find_le(10)[1] == 'en.wikipedia.org'

    s.insert((10, 'en.wikipedia.org'))
    s.insert((20, 'en.wikipedia.org'))

    assert s.find_le(20)[1] == 'en.wikipedia.org'
    assert len(s) == 1
    assert len(s.keys) == 1
    assert len(s.values) == 1


def test_remove():
    s = SortedKeyValue(itemgetter(1), itemgetter(0))
    s.insert((0, 'en.wikipedia.org'))
    s.remove((0, 'en.wikipedia.org'))

    assert len(s) == 0
    assert len(s.keys) == 0
    assert len(s.values) == 0

    s.insert((20, 'en.wikipedia.org'))
    s.remove(('whatever', 'en.wikipedia.org'))

    assert len(s) == 0
    assert len(s.keys) == 0
    assert len(s.values) == 0
