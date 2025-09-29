r"""
You are given the root of a binary tree. Return the deepest node (the furthest
node from the root).

Example:

>>> #     a
>>> #    / \
>>> #   b   c
>>> #  /
>>> # d
>>> tuples = ((("d",), "b"), "a", ("c",))
>>> deepest(BinaryTree.from_tuples(tuples)).as_tuples()
('d',)

Explanation: d is the farthest, at depth 3.
"""

from __future__ import annotations

import unittest

from ds.binary_tree import BinaryTree, TupleBinaryTree


def deepest_depth(root: BinaryTree[str]) -> tuple[int, BinaryTree[str]]:
    if root.left and root.right:
        left_depth, left_descendant = deepest_depth(root.left)
        right_depth, right_descendant = deepest_depth(root.right)
        if left_depth < right_depth:
            return right_depth + 1, right_descendant
        else:
            return left_depth + 1, left_descendant
    elif root.left:
        depth, descendant = deepest_depth(root.left)
        return depth + 1, descendant
    elif root.right:
        depth, descendant = deepest_depth(root.right)
        return depth + 1, descendant
    else:
        return 0, root


def deepest(root: BinaryTree[str]) -> BinaryTree[str]:
    return deepest_depth(root)[1]


class Tests(unittest.TestCase):
    cases: list[tuple[TupleBinaryTree[str], TupleBinaryTree[str]]] = [
        (("a",), ("a",)),
        ((("b",), "a"), ("b",)),
        ((("b",), "a", ("c",)), ("b",)),
        ((("b",), "a", (("d",), "c")), ("d",)),
    ]

    def test_cases(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                self.assertEqual(
                    BinaryTree.from_tuples(expected),
                    deepest(BinaryTree.from_tuples(root)),
                )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
