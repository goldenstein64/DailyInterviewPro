r"""
Given a sorted list of numbers, change it into a balanced binary search tree.
You can assume there will be no duplicate numbers in the list.

Example:

>>> create_bst([1, 2, 3, 4, 5, 6, 7]).as_tuples()
(((1,), 2, (3,)), 4, ((5,), 6, (7,)))

   4
  / \
 2   6
/ \ / \
1 3 5 7
"""

from __future__ import annotations

import unittest

from ds.binary_tree import BinaryTree, TupleBinaryTree


def create_bst_slice(values: list[int], i: int, j: int) -> BinaryTree[int] | None:
    """Create a binary search tree from values[i:j]."""
    if i >= j:
        return None

    mid = (i + j) // 2
    return BinaryTree(
        val=values[mid],
        left=create_bst_slice(values, i, mid),
        right=create_bst_slice(values, mid + 1, j),
    )


def create_bst(values: list[int]) -> BinaryTree[int] | None:
    """Create a binary search tree from a sorted list of values."""
    return create_bst_slice(values, 0, len(values))


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], TupleBinaryTree[int] | None]] = [
        ([], None),
        ([1], (1,)),
        ([1, 2, 3], ((1,), 2, (3,))),
        (
            [1, 2, 3, 4, 5, 6, 7],
            (((1,), 2, (3,)), 4, ((5,), 6, (7,))),
        ),
    ]

    def test_cases(self):
        for values, expected in self.cases:
            with self.subTest(values=values, expected=expected):
                if expected is None:
                    self.assertIsNone(create_bst(values))
                else:
                    self.assertEqual(
                        BinaryTree.from_tuples(expected), create_bst(values)
                    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
