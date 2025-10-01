"""
You are given a doubly linked list. Determine if it is a palindrome.

Can you do this for a singly linked list?

Examples:

>>> is_palindrome(LinkedList.from_values("abba"))
True

>>> is_palindrome(LinkedList.from_values("abc"))
False
"""

import unittest
from collections.abc import Callable, Iterable
from itertools import product
from typing import Any, cast

from ds.linked_list import LinkedList  # FYI, LinkedList is a singly-linked list
from solutions._2025._07_july._11_linked_list_reverse import (
    reverse_loop as reverse_list,
)


def is_palindrome_inner[T](
    node: LinkedList[T], root: LinkedList[T]
) -> tuple[bool, LinkedList[T] | None]:
    if not node.next:  # this is the last node, compare to root value
        return node.val == root.val, root.next

    result, opposite = is_palindrome_inner(node.next, root)
    if not result or not opposite or node is opposite:
        # short-circuited or reached the middle of an odd-length list
        return result, None
    elif node.next is opposite:
        # reached the middle of an even-length list
        return node.val == opposite.val, None
    else:
        return node.val == opposite.val, opposite.next


def is_palindrome(root: LinkedList[Any]) -> bool:
    """
    Determine whether a linked list is a palindrome, i.e. symmetrical. This uses
    the call stack and two node references to compare two nodes at opposite ends
    to each other. This tries to reduce the number of comparisons by checking
    for equality up to the middle node(s).

    This has O(n) time complexity and O(n) space.
    """
    return is_palindrome_inner(root, root)[0]


def is_palindrome_iter(root: LinkedList[Any]) -> bool:
    """
    Determine whether a linked list is a palindrome, i.e. symmetrical. This uses
    a slow pointer and fast pointer to find the midpoint, compares

    This has O(n) time complexity and O(1) space.
    """
    if not root.next:
        return True

    mid: LinkedList[Any] = root
    end: LinkedList[Any] = root
    fast: LinkedList[Any] | None = root
    while fast and fast.next:
        mid = cast(LinkedList[Any], mid.next)
        end = fast.next
        fast = end.next  # note: this gets advanced twice!

    if fast:  # odd-length list
        # no need to compare `mid` to itself when computing `result`
        reverse_list(cast(LinkedList[Any], mid.next))
        end = fast
    else:  # even-length list
        reverse_list(mid)

    result: bool = all(node.val == opp.val for node, opp in zip(root, end))
    reverse_list(end)
    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[LinkedList[Any]], bool]] = [
        is_palindrome,
        is_palindrome_iter,
    ]

    cases: list[tuple[Iterable[Any], bool]] = [
        ("a", True),
        ("aba", True),
        ("abba", True),
        ("abc", False),
        ("0123443210", True),
        ("racecar", True),
        ("tracecar", False),
    ]

    def test_cases(self):
        for solution, (values, expected) in product(self.solutions, self.cases):
            sol: str = solution.__name__
            with self.subTest(solution=sol, values=values, expected=expected):
                node = LinkedList.from_values(values, allow_empty=False)
                self.assertEqual(expected, solution(node))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
