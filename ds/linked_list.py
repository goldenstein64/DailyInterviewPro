from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass


@dataclass
class LinkedList[T]:
    """A container for a particular value in a linked list."""

    val: T
    next: LinkedList[T] | None = None
    """A pointer to the next Node."""

    @staticmethod
    def from_values[U](iterable: Iterable[U]) -> LinkedList[U] | None:
        """Generate a linked list from an iterable."""
        iterator: Iterator[U] = iter(iterable)
        try:
            head: LinkedList[U] = LinkedList(next(iterator))
        except StopIteration:
            return None

        node: LinkedList[U] = head
        for val in iterator:
            node.next = LinkedList(val)
            node = node.next

        return head

    def __iter__(self) -> Generator[LinkedList[T]]:
        node = self
        while node:
            yield node
            node = node.next

    def values(self) -> Generator[T]:
        return (node.val for node in self)

    def __str__(self) -> str:
        return " -> ".join(map(str, self.values()))
