"""
You are given a singly linked list and an integer k. Return the linked list,
removing the k-th last element from the list.

Try to do it in a single pass and using constant space.
"""

from __future__ import annotations

import unittest
from itertools import product
from typing import Callable, cast

from ds.linked_list import LinkedList


def remove_kth_from_linked_list(
    head: LinkedList[int], k: int
) -> LinkedList[int] | None:
    """
    Remove the kth element from the end of head. This implementation uses two
    passes: one to find the length and another to find the element that
    corresponds to k. The second
    """
    if k < 1:
        raise Exception("k must be greater than 0")

    length: int = 0
    node: LinkedList[int] | None = head
    while node:
        length += 1
        node = node.next

    if k > length:
        raise Exception("k must be at most the length of the list")

    rev_k = length - k + 1

    if rev_k == 1:
        return head.next

    prev_node: LinkedList[int] = head
    node: LinkedList[int] | None = head
    while node and rev_k > 1:
        prev_node = node
        node = node.next
        rev_k -= 1

    if node is None:
        raise Exception("k must be greater than 0")

    prev_node.next = node.next

    return head


def remove_kth_from_linked_list_gpt(
    head: LinkedList[int], k: int
) -> LinkedList[int] | None:
    """
    An implementation given to me by ChatGPT. It's known as the "two-pointer
    technique". It effectively uses between one and two passes if we're counting
    by the number of pointer re-directions: the front makes one complete pass,
    while the back passes len(head) - k nodes.
    """
    if k < 1:
        raise Exception("k must be greater than 0")

    dummy = LinkedList(-1, head)
    front: LinkedList[int] | None = dummy
    back: LinkedList[int] | None = dummy

    for _ in range(k + 1):
        if not front:
            raise Exception("k must be at most the length of the list")
        front = front.next

    while front:
        front = front.next
        back = cast(LinkedList[int], back.next)

    back.next = cast(LinkedList[int], back.next).next

    return dummy.next


class Tests(unittest.TestCase):
    solutions: list[Callable[[LinkedList[int], int], LinkedList[int] | None]] = [
        remove_kth_from_linked_list,
        remove_kth_from_linked_list_gpt,
    ]

    cases: list[tuple[list[int], int, list[int] | None | Exception]] = [
        ([1], 0, Exception("k must be greater than 0")),
        ([1], 1, None),
        ([1], 2, Exception("k must be at most the length of the list")),
        ([1, 2], 1, [1]),
        ([1, 2], 2, [2]),
        ([1, 2, 3], 1, [1, 2]),
        ([1, 2, 3], 2, [1, 3]),
        ([1, 2, 3], 3, [2, 3]),
        ([1, 2, 3, 4, 5], -1, Exception("k must be greater than 0")),
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 3, [1, 2, 4, 5]),
        ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 6, Exception("k must be at most the length of the list")),
    ]

    def test_cases(self):
        for solution, (values, k, expected) in product(self.solutions, self.cases):
            name = solution.__name__
            with self.subTest(solution=name, head=values, k=k, expected=expected):
                if isinstance(expected, Exception):
                    with self.assertRaises(Exception) as e:
                        node = LinkedList.from_values(values, allow_empty=False)
                        actual_node = solution(node, k)

                    self.assertEqual(expected.args, e.exception.args)
                else:
                    node = LinkedList.from_values(values, allow_empty=False)
                    actual_node = solution(node, k)
                    actual = [*actual_node.values()] if actual_node else None
                    self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
