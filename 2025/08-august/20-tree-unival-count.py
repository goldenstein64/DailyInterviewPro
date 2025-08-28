"""
A unival tree is a tree where all the nodes have the same value. Given a binary
tree, return the number of unival subtrees in the tree.

Example:

>>> count_unival_subtrees(
...     Node.from_tuples(
...         (
...             (1,),  # 1
...             0,
...             (
...                 ((1,), 1, (1,)),  # 2, 3, 4
...                 0,
...                 (0,),  # 5
...             ),
...         ),
...     ),
... )
5
"""

from __future__ import annotations

from dataclasses import dataclass


type TupleNode = (
    tuple[int]
    | tuple[TupleNode, int]
    | tuple[int, TupleNode]
    | tuple[TupleNode, int, TupleNode]
)


@dataclass
class Node:
    val: int
    left: Node | None = None
    right: Node | None = None

    @staticmethod
    def from_tuples(tuples: TupleNode) -> Node:
        match tuples:
            case (int(val),):
                return Node(val, None, None)
            case (tuple(left), int(val)):
                return Node(val, Node.from_tuples(left), None)
            case (int(val), tuple(right)):
                return Node(val, None, Node.from_tuples(right))
            case (tuple(left), int(val), tuple(right)):
                return Node(val, Node.from_tuples(left), Node.from_tuples(right))

    def as_tuples(self) -> TupleNode:
        match self:
            case Node(val, None, None):
                return (val,)
            case Node(val, Node() as left, None):
                return (left.as_tuples(), val)
            case Node(val, None, Node() as right):
                return (val, right.as_tuples())
            case Node(val, Node() as left, Node() as right):
                return (left.as_tuples(), val, right.as_tuples())
            case _:
                raise ValueError("unknown Node structure")


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
