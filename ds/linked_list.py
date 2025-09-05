from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass


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
