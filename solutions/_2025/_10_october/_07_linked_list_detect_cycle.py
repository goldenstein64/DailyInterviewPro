"""
Given a linked list, determine if the linked list has a cycle in it. For
notation purposes, we use an integer pos which represents the zero-indexed
position where the tail connects to.

Example:

>>> ls = LinkedList.from_values(range(5))
>>> has_cycle(ls)
False
>>> last(ls).next = ls
>>> has_cycle(ls)
True


"""

import unittest
from ds.linked_list import LinkedList
from typing import Any


def last[T](ls: LinkedList[T]) -> LinkedList[T]:
    result: LinkedList[T] = ls
    node: LinkedList[T] | None = ls
    while node:
        result = node
        node = node.next

    return result


def has_cycle(ls: LinkedList[Any]) -> bool:
    seen: set[int] = {id(ls)}
    node: LinkedList[Any] | None = ls.next
    while node is not None and id(node) not in seen:
        seen.add(id(node))
        node = node.next

    return node is not None


class Tests(unittest.TestCase):
    def test_acyclic(self):
        ls: LinkedList[int] = LinkedList.from_values(range(5), allow_empty=False)
        self.assertFalse(has_cycle(ls))

    def test_cyclic(self):
        ls: LinkedList[int] = LinkedList.from_values(range(5), allow_empty=False)
        last(ls).next = ls
        self.assertTrue(has_cycle(ls))

    def test_mid_cycle(self):
        ls: LinkedList[int] = LinkedList.from_values(range(5), allow_empty=False)
        last(ls).next = ls.next and ls.next.next
        self.assertTrue(has_cycle(ls))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
