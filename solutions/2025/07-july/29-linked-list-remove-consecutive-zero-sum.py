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

from ds.linked_list import LinkedList


def remove_consecutive_zero_sum(node: LinkedList[int]) -> LinkedList[int] | None:
    first_node: LinkedList[int] | None = node
    prev_node: LinkedList[int] | None = None
    rolling_node: LinkedList[int] | None = node
    rolling_sum: int = 0
    sum_history: dict[int, LinkedList[int] | None] = {}
    while rolling_node:
        if rolling_sum in sum_history:
            found_node = sum_history[rolling_sum]
            if found_node is None:
                first_node = rolling_node
            else:
                found_node.next = rolling_node
        else:
            sum_history[rolling_sum] = prev_node

        rolling_sum += rolling_node.val
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

    def test_cases(self):
        for values, expected in self.cases:
            with self.subTest(node=values, expected=expected):
                node = LinkedList.from_values(values, allow_empty=False)
                actual_node = remove_consecutive_zero_sum(node)
                actual = None if actual_node is None else [*actual_node.values()]
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
