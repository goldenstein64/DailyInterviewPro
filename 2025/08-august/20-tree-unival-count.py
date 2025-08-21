"""
A unival tree is a tree where all the nodes have the same value. Given a binary
tree, return the number of unival subtrees in the tree.

Example:

>>> count_unival_subtrees(
...     Node(
...         val=0,
...         left=Node(1),
...         right=Node(
...             val=0,
...             left=Node(1, Node(1), Node(1)),
...             right=Node(0),
...         ),
...     ),
... )
5
"""

from __future__ import annotations

from dataclasses import dataclass


type TupleNode = tuple[int, TupleNode, TupleNode] | tuple[int, TupleNode] | int


@dataclass
class Node:
    val: int
    left: Node | None = None
    right: Node | None = None

    def str_buffer(self, buffer: list[str], depth: int) -> None:
        indent = "  " * depth
        if self.right:
            self.right.str_buffer(buffer, depth + 1)
            buffer.append(f"{indent} /")

        buffer.append(f"{indent}{self.val}")

        if self.left:
            buffer.append(f"{indent} \\")
            self.left.str_buffer(buffer, depth + 1)

    def __str__(self) -> str:
        buffer: list[str] = []

        self.str_buffer(buffer, 0)

        return "\n".join(buffer)


@dataclass
class UnivalProperties:
    unival: int | None
    count: int


def collect_unival(root: Node) -> UnivalProperties:
    val: int | None = root.val
    count: int = 0
    self_count: int = 1
    if root.left:
        left = collect_unival(root.left)
        count += left.count
        if left.unival is None or left.unival != val:
            val = None
            self_count = 0

    if root.right:
        right = collect_unival(root.right)
        count += right.count
        if right.unival is None or right.unival != val:
            val = None
            self_count = 0

    return UnivalProperties(val, count + self_count)


def count_unival_subtrees(root: Node) -> int:
    return collect_unival(root).count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
