"""
You are given two singly linked lists. The lists intersect at some node. Find,
and return the node. Note: the lists are acyclic.

Example:

>>> shared = LinkedList(3, LinkedList(4))
>>> A = LinkedList(1, LinkedList(2, shared))
>>> B = LinkedList(6, shared)
>>> intersection(A, B)
LinkedList(val=3, next=LinkedList(val=4, next=None))
"""

from __future__ import annotations

import unittest

from ds.linked_list import LinkedList


def intersection(a: LinkedList[int], b: LinkedList[int]) -> LinkedList[int]:
    shared_nodes: set[int] = set(map(id, a))
    return next(node for node in b if id(node) in shared_nodes)


class Tests(unittest.TestCase):
    def test_minimal(self):
        shared: LinkedList[int] = LinkedList(3)
        a: LinkedList[int] = LinkedList(1, shared)
        b: LinkedList[int] = LinkedList(2, shared)

        self.assertEqual(shared, intersection(a, b))

    def test_smoke(self):
        shared: LinkedList[int] = LinkedList(3, LinkedList(4))
        a: LinkedList[int] = LinkedList(1, LinkedList(2, shared))
        b: LinkedList[int] = LinkedList(6, shared)

        self.assertEqual(shared, intersection(a, b))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
