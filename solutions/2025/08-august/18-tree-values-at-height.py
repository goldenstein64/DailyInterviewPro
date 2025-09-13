r"""
Given a binary tree, return all values given a certain height h.

Example:

    1
   / \
  2   3
 / \   \
4   5   7
>>> tree = BinaryTree.from_tuples((((4,), 2, (5,)), 1, (3, (7,))))
>>> values_at_height(tree).as_tuples()
[4, 5, 7]
"""

from __future__ import annotations

import unittest
from collections import deque
from collections.abc import Callable
from itertools import product

from ds.binary_tree import BinaryTree, TupleBinaryTree


def values_at_height(root: BinaryTree[int] | None, height: int) -> list[int]:
    if not root or height < 1:
        return []
    elif height == 1:
        return [root.val]
    else:
        left_values = values_at_height(root.left, height - 1)
        right_values = values_at_height(root.right, height - 1)
        return left_values + right_values


def values_at_height_gpt(root: BinaryTree[int] | None, height: int) -> list[int]:
    if not root or height < 1:
        return []

    q = deque([(root, 1)])
    result: list[int] = []
    while q:
        node, level = q.popleft()
        if level == height:
            result.append(node.val)
        elif level < height:
            if node.left:
                q.append((node.left, level + 1))
            if node.right:
                q.append((node.right, level + 1))
    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[BinaryTree[int] | None, int], list[int]]] = [
        values_at_height,
        values_at_height_gpt,
    ]

    cases: list[tuple[TupleBinaryTree[int] | None, int, list[int]]] = [
        (None, 1, []),
        ((1,), 1, [1]),
        ((1,), 2, []),
        ((1,), 0, []),
        (((1,), 2, (3,)), 2, [1, 3]),
        (
            (((4,), 2, (5,)), 1, (3, (7,))),
            3,
            [4, 5, 7],
        ),
    ]

    def test_cases(self):
        for solution, (root, height, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(
                solution=sol, root=root, height=height, expected=expected
            ):
                if root is None:
                    self.assertEqual(expected, solution(None, height))
                else:
                    self.assertEqual(
                        expected, solution(BinaryTree.from_tuples(root), height)
                    )


if __name__ == "__main__":
    unittest.main()
