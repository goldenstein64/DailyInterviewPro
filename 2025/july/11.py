"""
Given a singly-linked list, reverse the list. This can be done iteratively or
recursively. Can you get both solutions?

Example:
    Input: 4 -> 3 -> 2 -> 1 -> 0 -> NULL
    Output: 0 -> 1 -> 2 -> 3 -> 4 -> NULL
"""

from __future__ import annotations

import unittest
from typing import Any
from dataclasses import dataclass


@dataclass
class ListNode:
    val: Any
    next: ListNode | None = None

    @staticmethod
    def from_values(val: Any, *rest: Any) -> ListNode:
        head = ListNode(val)
        node = head
        for value in rest:
            node.next = ListNode(value)
            node = node.next

        return head

    def clone(self):
        return ListNode(val=self.val, next=self.next.clone() if self.next else None)

    def __iter__(self):
        node: ListNode | None = self
        while node is not None:
            yield node
            node = node.next

    def __str__(self) -> str:
        return " -> ".join(str(node.val) for node in self)

    def last(self) -> ListNode:
        node: ListNode = self
        while node.next:
            node = node.next

        return node

    def reverse_iteratively(self) -> ListNode:
        prev_node = self
        next_node: ListNode | None = self.next
        self.next = None
        while next_node is not None:  # B, C
            next_node.next, prev_node, next_node = prev_node, next_node, next_node.next

        return prev_node

    def reverse_recursively(self, prev_node: ListNode | None = None) -> ListNode:
        next_node, self.next = self.next, prev_node
        return next_node.reverse_recursively(self) if next_node is not None else self


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
        self.assertEqual(value, value.clone())

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

    def test_iterative(self):
        for head, expected in self.cases():
            with self.subTest(head=head.clone()):
                last = head.last()
                head.reverse_iteratively()
                self.assertEqual(expected, last)

    def test_recursive(self):
        for head, expected in self.cases():
            with self.subTest(head=head.clone()):
                last = head.last()
                head.reverse_recursively()
                self.assertEqual(expected, last)


if __name__ == "__main__":
    unittest.main()
