"""
You are given the root of a binary search tree. Return true if it is a valid
binary search tree, and false otherwise. Recall that a binary search tree has
the property that all values in the left subtree are less than or equal to the
root, and all values in the right subtree are greater than or equal to the root.
"""

from __future__ import annotations

import unittest

from ds.binary_tree import BinaryTree, TupleBinaryTree


def is_bst(
    root: BinaryTree[int] | None, lo: int | None = None, hi: int | None = None
) -> bool:
    if root is None:
        return True

    if lo is not None and lo > root.val:
        return False

    if hi is not None and root.val > hi:
        return False

    return is_bst(root.left, lo, root.val) and is_bst(root.right, root.val, hi)


class Tests(unittest.TestCase):
    cases: list[tuple[TupleBinaryTree[int] | None, bool]] = [
        (None, True),
        ((1,), True),
        (((1,), 1), True),
        ((1, (1,)), True),
        (((2,), 1), False),
        (((1,), 2, (3,)), True),
        (((3,), 2, (1,)), False),
        (
            (((1,), 3, (4,)), 5, ((6,), 7)),
            True,
        ),
        (
            (((1,), 3, (4,)), 5, ((8,), 7)),
            False,
        ),
    ]

    def test_cases(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                if root is None:
                    self.assertEqual(expected, is_bst(None))
                else:
                    self.assertEqual(expected, is_bst(BinaryTree.from_tuples(root)))


if __name__ == "__main__":
    unittest.main()
