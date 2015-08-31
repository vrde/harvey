import pytest
from harvey.heap import InMemoryHeap


def test_in_memory_heap_push_and_pop(monkeypatch):
    h = InMemoryHeap()
    h.push(1, 'cat')
    h.push(10, 'dog')

    assert h.pop() == 'cat'
    assert h.pop() == 'dog'


def test_in_memory_heap_upsert_element(monkeypatch):
    h1 = InMemoryHeap()
    h1.push(1, 'cat')
    h1.push(10, 'dog')
    h1.push(100, 'cat')

    h1.pop()
    h1.pop()
    with pytest.raises(IndexError):
        h1.pop()

    h2 = InMemoryHeap()
    h2.push(1, 'cat')
    h2.push(10, 'dog')
    h2.push(100, 'cat')

    assert h2.pop() == 'dog'
    assert h2.pop() == 'cat'
