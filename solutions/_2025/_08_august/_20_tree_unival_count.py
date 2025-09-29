"""
A unival tree is a tree where all the nodes have the same value. Given a binary
tree, return the number of unival subtrees in the tree.

Example:

>>> count_unival_subtrees(
...     BinaryTree.from_tuples(
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

from ds.binary_tree import BinaryTree


@dataclass
class UnivalProperties:
    unival: int | None
    count: int


def collect_unival(root: BinaryTree[int]) -> UnivalProperties:
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


def count_unival_subtrees(root: BinaryTree[int]) -> int:
    return collect_unival(root).count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
