"""
You are given two linked-lists representing two non-negative integers. The
digits are stored in reverse order and each of their nodes contain a single
digit. Add the two numbers and return it as a linked list.

Examples:

>>> # 342 + 465 = 807
>>> list(sum_loop(ListNode.from_values(2, 4, 3), ListNode.from_values(5, 6, 4)))
[7, 0, 8]

>>> # 444 + 556 = 1000
>>> list(sum_loop(ListNode.from_values(4, 4, 4), ListNode.from_values(6, 5, 5)))
[0, 0, 0, 1]
"""

from __future__ import annotations

import unittest
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
from typing import Generator


@dataclass
class ListNode:
    """Definition for singly-linked list."""

    val: int
    next: ListNode | None = None

    def __iter__(self) -> Generator[int]:
        """
        Iterate through this ListNode and its subsequent values.

        >>> list(ListNode.from_values(1, 2, 3))
        [1, 2, 3]
        """
        node = self
        while node is not None:
            yield node.val
            node = node.next

    def __len__(self) -> int:
        """
        Retrieve the length of this list.

        >>> len(ListNode.from_values(1, 2, 3))
        3
        """
        node: ListNode | None = self
        result: int = 0
        while node is not None:
            result += 1
            node = node.next
        return result

    @staticmethod
    def from_values(first: int, *values: int) -> ListNode:
        """
        Create a ListNode from a sequence of values.

        >>> ListNode.from_values(1, 2, 3)
        ListNode(val=1, next=ListNode(val=2, next=ListNode(val=3, next=None)))
        """
        rolling = result = ListNode(val=first)
        for value in values:
            rolling.next = ListNode(val=value)
            rolling = rolling.next

        return result


def sum_rec(l1: ListNode, l2: ListNode, carry: int = 0) -> ListNode:
    result = ListNode(val=l1.val + l2.val + carry)
    carry = result.val // 10
    result.val %= 10
    if l1.next and l2.next:
        result.next = sum_rec(l1.next, l2.next, carry)
    elif l1.next:
        result.next = l1.next
        result.next.val += carry
    elif l2.next:
        result.next = l2.next
        result.next.val += carry
    elif carry > 0:
        result.next = ListNode(carry)

    return result


def sum_loop(l1: ListNode, l2: ListNode) -> ListNode:
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
    solutions: list[Callable[[ListNode, ListNode], ListNode]] = [
        sum_rec,
        sum_loop,
    ]

    cases: list[tuple[ListNode, ListNode, ListNode]] = [
        (ListNode(0), ListNode(0), ListNode(0)),
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
    ]

    def test_cases(self):
        for solution, (l1, l2, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, l1=list(l1), l2=list(l2)):
                self.assertEqual(expected, solution(l1, l2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
