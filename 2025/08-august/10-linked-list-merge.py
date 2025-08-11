"""
You are given an array of k sorted singly linked lists. Merge the linked lists
into a single sorted linked list and return it.

Example:
    Input:
        - 1 -> 3 -> 5
        - 2 -> 4 -> 6
    Output: 1 -> 2 -> 3 -> 4 -> 5 -> 6
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from itertools import product
from operator import lt
from typing import (TYPE_CHECKING, Any, Generator, Iterable, Iterator,
                    Protocol, cast, override)

if TYPE_CHECKING:
    from _typeshed import (SupportsDunderGE, SupportsDunderGT,
                           SupportsDunderLE, SupportsDunderLT)

    type Comparable = (
        SupportsDunderLT[Any]
        | SupportsDunderGT[Any]
        | SupportsDunderLE[Any]
        | SupportsDunderGE[Any]
    )


@dataclass
class Node[T]:
    """A container for a particular value in a linked list."""

    val: T
    next: Node[T] | None = None
    """A pointer to the next Node."""

    @staticmethod
    def from_values[S](iterable: Iterable[S]) -> Node[S] | None:
        """Generate a linked list from an iterable."""
        iterator: Iterator[S] = iter(iterable)
        try:
            head: Node[S] = Node(next(iterator))
        except StopIteration:
            return None

        node: Node[S] = head
        for val in iterator:
            node.next = Node(val)
            node = node.next

        return head

    def __iter__(self) -> Generator[Node[T]]:
        node = self
        while node:
            yield node
            node = node.next

    def values(self) -> Generator[T]:
        return (node.val for node in self)

    def __str__(self) -> str:
        return " -> ".join(map(str, self.values()))


class Solution(Protocol):
    def merge[T: Comparable](self, lists: list[Node[T]]) -> Node[T] | None: ...


class SolutionPure(Solution):
    """My pure implementation of the solution."""

    def merge_two[T: Comparable](
        self, a: Node[T] | None, b: Node[T] | None
    ) -> Node[T] | None:
        dummy: Node[T] = Node(cast(T, None))
        last: Node[T] = dummy
        while a and b:
            if lt(a.val, b.val):
                last.next = Node(a.val)
                a = a.next
            else:
                last.next = Node(b.val)
                b = b.next
            last = last.next

        last.next = a or b

        return dummy.next

    def merge_multiple[T: Comparable](
        self, lists: list[Node[T]], i: int, j: int
    ) -> Node[T] | None:
        if j - i == 1:
            return lists[i]

        mid = (i + j) // 2
        return self.merge_two(
            self.merge_multiple(lists, i, mid),
            self.merge_multiple(lists, mid, j),
        )

    def merge[T: Comparable](self, lists: list[Node[T]]) -> Node[T] | None:
        """
        Merge a list of sorted linked lists. This uses an algorithm similar to merge
        sort, recursively splitting the list in half and merging each half into the
        result.
        """
        return self.merge_multiple(lists, 0, len(lists)) if lists else None


class SolutionInPlace(SolutionPure, Solution):
    """My in-place implementation of the solution."""

    @override
    def merge_two[T: Comparable](
        self, a: Node[T] | None, b: Node[T] | None
    ) -> Node[T] | None:
        dummy: Node[T] = Node(cast(T, None))
        last: Node[T] = dummy
        while a and b:
            if lt(a.val, b.val):
                last.next = a
                a = a.next
            else:
                last.next = b
                b = b.next
            last = last.next

        last.next = a or b

        return dummy.next


class Tests(unittest.TestCase):
    solutions: list[type[Solution]] = [SolutionPure, SolutionInPlace]

    cases: list[tuple[list[list[int]], list[int] | None]] = [
        ([], None),
        ([[]], None),
        ([[], []], None),
        ([[2], [1]], [1, 2]),
        ([[1, 3, 5], [2, 4, 6]], [1, 2, 3, 4, 5, 6]),
        ([[1, 4, 7], [3, 6, 9], [2, 5, 8]], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([[4, 8], [3, 7], [2, 6], [1, 5]], [1, 2, 3, 4, 5, 6, 7, 8]),
    ]

    def test_all(self):
        for solution, (lists_values, expected) in product(self.solutions, self.cases):
            with self.subTest(lists=lists_values, expected=expected):
                lists: list[Node[int]] = list(
                    filter(None, map(Node.from_values, lists_values))
                )
                actual: Node[int] | None = solution().merge(lists)
                self.assertEqual(expected, actual and list(actual.values()))


if __name__ == "__main__":
    unittest.main()
