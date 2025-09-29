"""
You are given two linked-lists representing two non-negative integers. The
digits are stored in reverse order and each of their nodes contain a single
digit. Add the two numbers and return it as a linked list.

Examples:

>>> # 342 + 465 = 807
>>> res = sum_loop(LinkedList.from_values([2, 4, 3]), LinkedList.from_values([5, 6, 4]))
>>> list(res.values())
[7, 0, 8]

>>> # 444 + 556 = 1000
>>> res = sum_loop(LinkedList.from_values([4, 4, 4]), LinkedList.from_values([6, 5, 5]))
>>> list(res.values())
[0, 0, 0, 1]
"""

from __future__ import annotations

import unittest
from collections.abc import Callable
from itertools import product

from ds.linked_list import LinkedList


def sum_rec(
    l1: LinkedList[int], l2: LinkedList[int], carry: int = 0
) -> LinkedList[int]:
    result = LinkedList[int](val=l1.val + l2.val + carry)
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
        result.next = LinkedList(carry)

    return result


def sum_loop(l1: LinkedList[int], l2: LinkedList[int]) -> LinkedList[int]:
    rolling = result = LinkedList(l1.val + l2.val)
    carry = rolling.val // 10
    rolling.val %= 10
    rolling1: LinkedList[int] | None = l1.next
    rolling2: LinkedList[int] | None = l2.next
    while rolling1 or rolling2:
        if rolling1 and rolling2:
            rolling.next = LinkedList(rolling1.val + rolling2.val + carry)
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
        rolling.next = LinkedList(1)

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[LinkedList[int], LinkedList[int]], LinkedList[int]]] = [
        sum_rec,
        sum_loop,
    ]

    cases: list[tuple[LinkedList[int], LinkedList[int], LinkedList[int]]] = [
        (LinkedList(0), LinkedList(0), LinkedList(0)),
        (
            LinkedList.from_values([2, 4, 3], allow_empty=False),
            LinkedList.from_values([5, 6, 4], allow_empty=False),
            LinkedList.from_values([7, 0, 8], allow_empty=False),
        ),
        (
            LinkedList.from_values([4, 4, 4], allow_empty=False),
            LinkedList.from_values([6, 5, 5], allow_empty=False),
            LinkedList.from_values([0, 0, 0, 1], allow_empty=False),
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
