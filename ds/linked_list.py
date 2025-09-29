from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass
from typing import Literal, overload
import unittest


@dataclass
class LinkedList[T]:
    """a container for a particular value in a linked list"""

    val: T
    next: LinkedList[T] | None = None
    """a pointer to the next linked list node"""

    @overload
    @staticmethod
    def from_values[U](
        iterable: Iterable[U], *, allow_empty: Literal[False]
    ) -> LinkedList[U]: ...
    @overload
    @staticmethod
    def from_values[U](
        iterable: Iterable[U], *, allow_empty: Literal[True] = True
    ) -> LinkedList[U] | None: ...
    @staticmethod
    def from_values[U](
        iterable: Iterable[U], *, allow_empty: bool = True
    ) -> LinkedList[U] | None:
        """Generate a linked list from an iterable."""
        iterator: Iterator[U] = iter(iterable)
        try:
            head: LinkedList[U] = LinkedList(next(iterator))
        except StopIteration:
            if allow_empty:
                return None
            else:
                raise ValueError

        node: LinkedList[U] = head
        for val in iterator:
            node.next = LinkedList(val)
            node = node.next

        return head

    def __iter__(self) -> Generator[LinkedList[T]]:
        """Iterate through every node in this linked list."""
        node = self
        while node:
            yield node
            node = node.next

    def values(self) -> Generator[T]:
        """Iterate through every value in this linked list."""
        return (node.val for node in self)

    def __str__(self) -> str:
        return " -> ".join(map(str, self.values()))


class Tests(unittest.TestCase):
    def test_clone(self):
        value: LinkedList[int] = LinkedList(
            val=4,
            next=LinkedList(
                val=3,
                next=LinkedList(val=2, next=LinkedList(val=1, next=LinkedList(val=0))),
            ),
        )
        self.assertEqual(value, LinkedList.from_values(value.values()))

    def test_from_values(self):
        expected = LinkedList(
            10,
            LinkedList(
                5,
                LinkedList(
                    -3, LinkedList(-3, LinkedList(1, LinkedList(4, LinkedList(-4))))
                ),
            ),
        )
        self.assertEqual(expected, LinkedList.from_values([10, 5, -3, -3, 1, 4, -4]))

    def test_values(self):
        expected = [10, 5, -3, -3, 1, 4, -4]
        self.assertEqual(
            expected,
            list(
                LinkedList.from_values(
                    [10, 5, -3, -3, 1, 4, -4], allow_empty=False
                ).values()
            ),
        )


if __name__ == "__main__":
    unittest.main()
