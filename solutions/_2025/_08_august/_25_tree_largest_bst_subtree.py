"""
You are given the root of a binary tree. Find and return the largest subtree of
that tree, which is a valid binary search tree.

Examples:

>>> largest_bst_subtree(BinaryTree(1)).as_tuples()
(1,)

>>> node = BinaryTree.from_tuples(((1,), 1))
>>> largest_bst_subtree(node).as_tuples()
(1,)

>>> node = BinaryTree.from_tuples(((1,), 2, (3,)))
>>> largest_bst_subtree(node).as_tuples()
((1,), 2, (3,))

>>> node = BinaryTree.from_tuples(
...     (((2,), 6), 5, ((4,), 7, (9,)))
... )
>>> largest_bst_subtree(node).as_tuples()
((4,), 7, (9,))

>>> node = BinaryTree.from_tuples(
...     (((2,), 4), 5, ((6,), 7, (9,)))
... )
>>> largest_bst_subtree(node).as_tuples()
(((2,), 4), 5, ((6,), 7, (9,)))
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from operator import attrgetter

from ds.binary_tree import BinaryTree, TupleBinaryTree


@dataclass
class BSTSubtreeResult:
    """an internal data structure for the largest_bst_subtree algorithm"""

    node: BinaryTree[int]
    size: int
    min: int
    max: int


def largest_bst_subtree_inner(root: BinaryTree[int]) -> BSTSubtreeResult:
    match (root.left, root.right):
        case (BinaryTree() as left, BinaryTree() as right):
            subtree_left = largest_bst_subtree_inner(left)
            subtree_right = largest_bst_subtree_inner(right)
            # try to expand the tree
            if (
                subtree_left.node == left
                and subtree_right.node == right
                and root.val > subtree_left.max
                and root.val < subtree_right.min
            ):
                return BSTSubtreeResult(
                    node=root,
                    size=subtree_left.size + subtree_right.size + 1,
                    min=subtree_left.min,
                    max=subtree_right.max,
                )

            return max(subtree_left, subtree_right, key=attrgetter("size"))
        case (BinaryTree() as left, None):
            subtree = largest_bst_subtree_inner(left)
            # try to expand the tree
            if subtree.node == left and root.val > subtree.max:
                return BSTSubtreeResult(
                    node=root,
                    size=subtree.size + 1,
                    min=subtree.min,
                    max=root.val,
                )

            return subtree
        case (None, BinaryTree() as right):
            subtree = largest_bst_subtree_inner(right)
            # try to expand the tree
            if subtree.node == right and root.val < subtree.min:
                return BSTSubtreeResult(
                    node=root,
                    size=subtree.size + 1,
                    min=root.val,
                    max=subtree.max,
                )

            return subtree
        case (None, None):
            return BSTSubtreeResult(node=root, size=1, min=root.val, max=root.val)


def largest_bst_subtree(root: BinaryTree[int]) -> BinaryTree[int]:
    """
    Return the largest binary search tree subtree of `root`.

    Generally, we can start at a leaf node, move up to its parent, and if the
    parent and other branch is on the correct side of the search tree, then the
    entire thing can be a binary search tree
    """
    return largest_bst_subtree_inner(root).node


class Tests(unittest.TestCase):
    cases: list[tuple[TupleBinaryTree[int], TupleBinaryTree[int]]] = [
        ((1,), (1,)),
        (((1,), 1), (1,)),
        ((1, (1,)), (1,)),
        ((1, (0,)), (0,)),
        ((((10,), 5), 2, (1,)), (10,)),
        (((1,), 2, (3,)), ((1,), 2, (3,))),
        (((2,), 1, (3,)), (2,)),
        ((((2,), 6), 5, ((4,), 7, (9,))), ((4,), 7, (9,))),
        ((((2,), 4), 5, ((6,), 7, (9,))), (((2,), 4), 5, ((6,), 7, (9,)))),
    ]

    def test_cases(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                self.assertEqual(
                    BinaryTree.from_tuples(expected),
                    largest_bst_subtree(BinaryTree.from_tuples(root)),
                )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
