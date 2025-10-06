r"""
You are given the root of a binary tree, along with two nodes, A and B. Find and
return the lowest common ancestor of A and B. For this problem, you can assume
that each node also has a pointer to its parent, along with its left and right
child.

Example:

#   a
#  / \
# b   c
#    / \
#   d*  e*
>>> root = BinaryTree.from_tuples((("b",), "a", (("d",), "c", ("e",))))
>>> d = root.right.left
>>> e = root.right.right
>>> c = lowest_common_ancestor(root, d, e)
>>> c.val
'c'
"""

import unittest
from collections.abc import Callable
from itertools import product
from typing import Any

from ds.binary_tree import BinaryTree, TupleBinaryTree


def lowest_common_ancestor(
    root: BinaryTree[Any], a: BinaryTree[Any], b: BinaryTree[Any]
) -> BinaryTree[Any] | None:
    if a is b:
        return a

    a_ancestors: set[int] = set(map(id, a.ancestors()))
    return next((n for n in b.ancestors() if id(n) in a_ancestors), None)


def lowest_common_ancestor_lists(
    root: BinaryTree[Any], a: BinaryTree[Any], b: BinaryTree[Any]
) -> BinaryTree[Any] | None:
    if a is b:
        return a

    a_ancestors = list(a.ancestors())
    b_ancestors = list(b.ancestors())
    last_node: BinaryTree[Any] | None = None
    for a_node, b_node in zip(reversed(a_ancestors), reversed(b_ancestors)):
        if a_node is b_node:
            last_node = a_node

    return last_node


class Tests(unittest.TestCase):
    solutions: list[
        Callable[
            [BinaryTree[Any], BinaryTree[Any], BinaryTree[Any]], BinaryTree[Any] | None
        ]
    ] = [
        lowest_common_ancestor,
        lowest_common_ancestor_lists,
    ]

    cases: list[tuple[TupleBinaryTree[Any], str, str, str]] = [
        (("a",), "", "", ""),
        (("a", ("b", ("c",))), "R", "RR", "R"),
        (("a", ("b", ("c",))), "", "RR", ""),
        ((("b",), "a", (("d",), "c", ("e",))), "RL", "RR", "R"),
    ]

    def test_cases(self):
        for solution, (tuples, left_path, right_path, expected_path) in product(
            self.solutions, self.cases
        ):
            sol = solution.__name__
            with self.subTest(
                solution=sol,
                root=tuples,
                left=left_path,
                right=right_path,
                expected=expected_path,
            ):
                root: BinaryTree[Any] = BinaryTree.from_tuples(tuples)
                left: BinaryTree[Any] = root.path(left_path)
                right: BinaryTree[Any] = root.path(right_path)
                expected: BinaryTree[Any] = root.path(expected_path)
                assert left and right and expected
                self.assertIs(expected, solution(root, left, right))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
