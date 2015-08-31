"""
"""

import heapq


class Heap(object):

    def index(self, x):
        raise NotImplementedError

    def push(self, priority, element):
        raise NotImplementedError
        
    def pop(self):
        raise NotImplementedError

    def __contains__(self, element):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class InMemoryHeap(object):

    def __init__(self):
        self.heap = []
        self.elements = set()

    def index(self, x):
        for i, (priority, element) in enumerate(self.heap):
            if element == x:
                return i

    def push(self, priority, element):
        if element in self.elements:
            idx = self.index(element)
            self.heap[idx] = (priority, element)
            heapq.heapify(self.heap)
        else:
            heapq.heappush(self.heap, (priority, element))
            self.elements.add(element)

    def pop(self):
        """Pop an element form the heap.

        Raise IndexError if the heap is empty.
        """

        priority, element = heapq.heappop(self.heap)
        self.elements.remove(element)
        return element

    def __contains__(self, element):
        return element in self.elements
    
    def __len__(self):
        return len(self.elements)
