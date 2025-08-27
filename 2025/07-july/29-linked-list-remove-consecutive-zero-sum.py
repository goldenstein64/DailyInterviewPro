"""
Given a linked list of integers, remove all consecutive nodes that sum up to 0.

Example:

>>> remove_consecutive_zero_sum(Node.from_values([10, 5, -3, -3, 1, 4, -4]))
Node(value=10, next=None)

Explanation: The consecutive nodes 5 -> -3 -> -3 -> 1 sums up to 0 so that
sequence should be removed. 4 -> -4 also sums up to 0 so that sequence should
also be removed.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass
class Node:
    value: int
    next: Node | None = None

    @staticmethod
    def from_values(values: Iterable[int]) -> Node:
        it = iter(values)

        first_node: Node = Node(next(it))
        last_node: Node = first_node
        for val in it:
            node = Node(val)
            last_node.next = node
            last_node = node

        return first_node

    def __iter__(self) -> Iterator[Node]:
        node = self
        while node:
            yield node
            node = node.next

    def values(self) -> Iterator[int]:
        return (node.value for node in self)

    @staticmethod
    def repr(node: Node | None) -> list[int] | None:
        return [*node.values()] if node else None


def remove_consecutive_zero_sum(node: Node) -> Node | None:
    first_node: Node | None = node
    prev_node: Node | None = None
    rolling_node: Node | None = node
    rolling_sum: int = 0
    sum_history: dict[int, Node | None] = {}
    while rolling_node:
        if rolling_sum in sum_history:
            found_node = sum_history[rolling_sum]
            if found_node is None:
                first_node = rolling_node
            else:
                found_node.next = rolling_node
        else:
            sum_history[rolling_sum] = prev_node

        rolling_sum += rolling_node.value
        prev_node, rolling_node = rolling_node, rolling_node.next

    if rolling_sum in sum_history:
        found_node = sum_history[rolling_sum]
        if found_node is None:
            first_node = None
        else:
            found_node.next = None

    return first_node


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], list[int] | None]] = [
        ([0], None),
        ([10, 0], [10]),
        ([0, 10], [10]),
        ([0, 10, 0], [10]),
        ([0, 0], None),
        ([1, -1, 2, -2], None),
        ([5, -5, 10, 6, -6], [10]),
        ([10, 5, -3, -3, 1, 4, -4], [10]),
    ]

    def test_from_values(self):
        expected = Node(10, Node(5, Node(-3, Node(-3, Node(1, Node(4, Node(-4)))))))
        self.assertEqual(expected, Node.from_values([10, 5, -3, -3, 1, 4, -4]))

    def test_values(self):
        expected = [10, 5, -3, -3, 1, 4, -4]
        self.assertEqual(
            expected, list(Node.from_values([10, 5, -3, -3, 1, 4, -4]).values())
        )

    def test_all(self):
        for values, expected in self.cases:
            with self.subTest(node=values, expected=expected):
                node = Node.from_values(values)
                actual_node = remove_consecutive_zero_sum(node)
                actual = None if actual_node is None else [*actual_node.values()]
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
