r"""
You are given the root of a binary tree. Find the path between 2 nodes that
maximizes the sum of all the nodes in the path, and return the sum. The path
does not necessarily need to go through the root.

Example:

(* denotes the max path)
      *10
      /  \
    *2   *10
    / \     \
  *20  1    -25
            /  \
           3    4
>>> tree = BinaryTree.from_tuples(
...     (
...         ((20,), 2, (1,)),
...         10,
...         (10, ((3,), -25, (4,))),
...     ),
... )
>>> max_path_sum(tree)
42
"""

from collections.abc import Callable
from ds.binary_tree import BinaryTree, TupleBinaryTree
from itertools import product
import unittest
from sys import maxsize


def max_path_sum_inner(root: BinaryTree[int]) -> tuple[int, int]:
    """
    First return is the max joint sum, second return is the max disjoint sum.
    The max joint sum refers to the maximum possible value for a given path
    starting at the root. The max disjoint sum refers to the maximum possible
    value for a path that doesn't necessarily start at the root.
    """

    val: int = root.val
    match (root.left, root.right):
        case (BinaryTree() as left, BinaryTree() as right):
            left_joint, left_disjoint = max_path_sum_inner(left)
            right_joint, right_disjoint = max_path_sum_inner(right)
            joint_max: int = val + max(0, left_joint, right_joint)
            return joint_max, max(
                joint_max,
                val + left_joint + right_joint,
                left_disjoint,
                right_disjoint,
            )
        case (BinaryTree() as left, None):
            left_joint, left_disjoint = max_path_sum_inner(left)
            joint_max: int = val + max(0, left_joint)
            return joint_max, max(joint_max, left_disjoint)
        case (None, BinaryTree() as right):
            right_joint, right_disjoint = max_path_sum_inner(right)
            joint_max: int = val + max(0, right_joint)
            return joint_max, max(joint_max, right_disjoint)
        case (None, None):
            return val, val


def max_path_sum(root: BinaryTree[int]) -> int:
    return max_path_sum_inner(root)[1]


def max_path_sum_gpt(root: BinaryTree[int]) -> int:
    max_sum: int = -maxsize

    def dfs(node: BinaryTree[int] | None) -> int:
        nonlocal max_sum
        if not node:
            return 0

        left_gain = max(0, dfs(node.left))
        right_gain = max(0, dfs(node.right))

        max_sum = max(max_sum, node.val + left_gain + right_gain)

        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum


class Tests(unittest.TestCase):
    solutions: list[Callable[[BinaryTree[int]], int]] = [
        max_path_sum,
        max_path_sum_gpt,
    ]

    cases: list[tuple[TupleBinaryTree[int], int]] = [
        ((10,), 10),
        (((1,), 2), 3),
        (((1,), -2), 1),
        (((-1,), 2), 2),
        (((-1,), -2), -1),
        ((1, (2,)), 3),
        ((1, (-2,)), 1),
        ((-1, (2,)), 2),
        ((-1, (-2,)), -1),
        (((1,), 2, (3,)), 6),
        (((1,), -2, (3,)), 3),
        (((-1,), 2, (3,)), 5),
        (((1,), 2, (-3,)), 3),
        (((-1,), 2, (-3,)), 2),
        (((-1,), -2, (3,)), 3),
        (((1,), -2, (-3,)), 1),
        (((-1,), -2, (-3,)), -1),
        (
            (
                ((20,), 2, (1,)),
                10,
                (10, ((3,), -25, (4,))),
            ),
            42,
        ),
    ]

    def test_cases(self):
        for solution, (tuple_root, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, root=tuple_root, expected=expected):
                root = BinaryTree.from_tuples(tuple_root)
                self.assertEqual(expected, solution(root))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
