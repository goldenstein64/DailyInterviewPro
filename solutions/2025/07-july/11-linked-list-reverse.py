"""
Given a singly-linked list, reverse the list. This can be done iteratively or
recursively. Can you get both solutions?

Example:

>>> ls = ListNode.from_values(4, 3, 2, 1, 0)
>>> list(ls)
[4, 3, 2, 1, 0]
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Any


@dataclass
class ListNode:
    val: Any
    next: ListNode | None = None

    @staticmethod
    def from_values(val: Any, *rest: Any) -> ListNode:
        """
        Create a ListNode from a sequence of values

        >>> ls = ListNode.from_values(1, 2, 3)
        >>> list(ls)
        [1, 2, 3]
        """
        head = ListNode(val)
        node = head
        for value in rest:
            node.next = ListNode(value)
            node = node.next

        return head

    def copy(self):
        return ListNode(val=self.val, next=self.next.copy() if self.next else None)

    def __iter__(self):
        """
        Iterate through the values of this ListNode.

        >>> ls = ListNode(1, ListNode(2, ListNode(3)))
        >>> list(ls)
        [1, 2, 3]
        """
        node: ListNode | None = self
        while node is not None:
            yield node.val
            node = node.next

    def __str__(self) -> str:
        """
        Return a string representation of this ListNode.

        >>> ls = ListNode.from_values(1, 2, 3)
        >>> str(ls)
        '1 -> 2 -> 3'
        """
        return " -> ".join(map(str, self))

    def last(self) -> ListNode:
        node: ListNode = self
        while node.next:
            node = node.next

        return node

    def reverse_loop(self) -> None:
        prev_node = self
        next_node: ListNode | None = self.next
        self.next = None
        while next_node is not None:  # B, C
            next_node.next, prev_node, next_node = prev_node, next_node, next_node.next

    def reverse_rec(self, prev_node: ListNode | None = None) -> None:
        next_node, self.next = self.next, prev_node
        if next_node:
            next_node.reverse_rec(self)


class Tests(unittest.TestCase):
    @staticmethod
    def cases() -> list[tuple[ListNode, ListNode]]:
        return [
            (ListNode.from_values(1), ListNode.from_values(1)),
            (ListNode.from_values(4, 3, 2, 1, 0), ListNode.from_values(0, 1, 2, 3, 4)),
        ]

    def test_clone(self):
        value = ListNode(
            val=4,
            next=ListNode(
                val=3,
                next=ListNode(val=2, next=ListNode(val=1, next=ListNode(val=0))),
            ),
        )
        self.assertEqual(value, value.copy())

    def test_from_values(self):
        self.assertEqual(
            ListNode(
                val=4,
                next=ListNode(
                    val=3,
                    next=ListNode(val=2, next=ListNode(val=1, next=ListNode(val=0))),
                ),
            ),
            ListNode.from_values(4, 3, 2, 1, 0),
        )

    def test_loop(self):
        for head, expected in self.cases():
            with self.subTest(head=head.copy()):
                last = head.last()
                head.reverse_loop()
                self.assertEqual(expected, last)

    def test_rec(self):
        for head, expected in self.cases():
            with self.subTest(head=head.copy()):
                last = head.last()
                head.reverse_rec()
                self.assertEqual(expected, last)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    unittest.main()
