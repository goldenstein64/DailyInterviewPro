"""
You are given two linked-lists representing two non-negative integers. The
digits are stored in reverse order and each of their nodes contain a single
digit. Add the two numbers and return it as a linked list.

Example:

    Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
    Output: 7 -> 0 -> 8
    Explanation: 342 + 465 = 807.

    Input: (4 -> 4 -> 4) + (6 -> 5 -> 5)
    Output: (0 -> 0 -> 0 -> 1)
    Explanation: 444 + 556 = 1000
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Generator


@dataclass
class ListNode:
    """Definition for singly-linked list."""

    val: int
    next: ListNode | None = None

    def __iter__(self) -> Generator[int]:
        node = self
        while node is not None:
            yield node.val
            node = node.next

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        node: ListNode | None = self
        result: int = 0
        while node is not None:
            result += 1
            node = node.next
        return result

    @staticmethod
    def from_values(first: int, *values: int) -> ListNode:
        rolling = result = ListNode(val=first)
        for value in values:
            rolling.next = ListNode(val=value)
            rolling = rolling.next

        return result


class Solution:
    def sum_rec(self, l1: ListNode, l2: ListNode, carry: int = 0) -> ListNode:
        result = ListNode(val=l1.val + l2.val + carry)
        carry = result.val // 10
        result.val %= 10
        if l1.next and l2.next:
            result.next = self.sum_rec(l1.next, l2.next, carry)
        elif l1.next:
            result.next = l1.next
            result.next.val += carry
        elif l2.next:
            result.next = l2.next
            result.next.val += carry
        elif carry > 0:
            result.next = ListNode(carry)

        return result

    def sum_loop(self, l1: ListNode, l2: ListNode) -> ListNode:
        rolling = result = ListNode(l1.val + l2.val)
        carry = rolling.val // 10
        rolling.val %= 10
        rolling1: ListNode | None = l1.next
        rolling2: ListNode | None = l2.next
        while rolling1 or rolling2:
            if rolling1 and rolling2:
                rolling.next = ListNode(rolling1.val + rolling2.val + carry)
                rolling = rolling.next
                rolling1 = rolling1.next
                rolling2 = rolling2.next
                carry = rolling.val // 10
                rolling.val %= 10
            elif rolling1:
                rolling.next = rolling1
                break
            else:
                rolling.next = rolling2
                break

        if carry == 1:
            rolling.next = ListNode(1)

        return result


class Tests(unittest.TestCase):
    cases: tuple[tuple[ListNode, ListNode, ListNode], ...] = (
        (ListNode(val=0), ListNode(val=0), ListNode(val=0)),
        (
            ListNode.from_values(2, 4, 3),
            ListNode.from_values(5, 6, 4),
            ListNode.from_values(7, 0, 8),
        ),
        (
            ListNode.from_values(4, 4, 4),
            ListNode.from_values(6, 5, 5),
            ListNode.from_values(0, 0, 0, 1),
        ),
    )

    def test_all(self):
        for l1, l2, expected in self.cases:
            with self.subTest(l1=list(l1), l2=list(l2)):
                self.assertEqual(expected, Solution().sum_rec(l1, l2))
                self.assertEqual(expected, Solution().sum_loop(l1, l2))


if __name__ == "__main__":
    unittest.main()
