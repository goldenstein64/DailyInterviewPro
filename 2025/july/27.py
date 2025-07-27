"""
You are given two singly linked lists. The lists intersect at some node. Find,
and return the node. Note: the lists are acyclic.

Example:

A = 1 -> 2 -> 3 -> 4
B = 6 -> 3 -> 4

This should return 3 (you may assume that any nodes with the same value are the
same node).
"""

from __future__ import annotations

from dataclasses import dataclass
import unittest
from typing import Generator


@dataclass
class Node:
    val: int
    next: Node | None = None

    def __iter__(self) -> Generator[Node]:
        node = self
        while node:
            yield node
            node = node.next


def intersection(a: Node, b: Node) -> Node:
    shared_nodes = set(id(node) for node in a)
    return next(node for node in b if id(node) in shared_nodes)


class Tests(unittest.TestCase):
    def test_minimal(self):
        shared = Node(3)
        a = Node(1, shared)
        b = Node(2, shared)

        self.assertEqual(shared, intersection(a, b))

    def test_smoke(self):
        shared = Node(3, Node(4))
        a = Node(1, Node(2, shared))
        b = Node(6, shared)

        self.assertEqual(shared, intersection(a, b))


if __name__ == "__main__":
    unittest.main()
