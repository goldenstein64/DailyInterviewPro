"""
Given a singly-linked list, reverse the list. This can be done iteratively or
recursively. Can you get both solutions?

Example:

>>> ls = LinkedList.from_values([4, 3, 2, 1, 0])
>>> list(ls.values())
[4, 3, 2, 1, 0]
>>> last_node = last(ls)
>>> reverse_rec(ls)
>>> list(last_node.values())
[0, 1, 2, 3, 4]
"""

from __future__ import annotations

import unittest
from typing import Any

from ds.linked_list import LinkedList


def last(node: LinkedList[Any]) -> LinkedList[Any]:
    while node.next:
        node = node.next

    return node


def reverse_loop(node: LinkedList[Any]) -> None:
    prev_node: LinkedList[Any] = node
    next_node: LinkedList[Any] | None = node.next
    node.next = None
    while next_node is not None:  # B, C
        next_node.next, prev_node, next_node = prev_node, next_node, next_node.next


def reverse_rec(
    node: LinkedList[Any], prev_node: LinkedList[Any] | None = None
) -> None:
    next_node, node.next = node.next, prev_node
    if next_node:
        reverse_rec(next_node, node)


class Tests(unittest.TestCase):
    @staticmethod
    def cases() -> list[tuple[LinkedList[Any], LinkedList[Any]]]:
        return [
            (LinkedList(1), LinkedList(1)),
            (
                LinkedList.from_values([4, 3, 2, 1, 0], allow_empty=False),
                LinkedList.from_values([0, 1, 2, 3, 4], allow_empty=False),
            ),
        ]

    def test_loop(self):
        for head, expected in self.cases():
            with self.subTest(head=list(head)):
                last_node = last(head)
                reverse_loop(head)
                self.assertEqual(expected, last_node)

    def test_rec(self):
        for head, expected in self.cases():
            with self.subTest(head=list(head)):
                last_node = last(head)
                reverse_rec(head)
                self.assertEqual(expected, last_node)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    unittest.main()
