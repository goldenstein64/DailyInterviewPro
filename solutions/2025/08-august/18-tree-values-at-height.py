r"""
Given a binary tree, return all values given a certain height h.

Example:
    Input:
            1
           / \
          2   3
         / \   \
        4   5   7
    Output: [4, 5, 7]
"""

from __future__ import annotations

import unittest
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product

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


def values_at_height(root: Node | None, height: int) -> list[int]:
    if not root or height < 1:
        return []
    elif height == 1:
        return [root.val]
    else:
        left_values = values_at_height(root.left, height - 1)
        right_values = values_at_height(root.right, height - 1)
        return left_values + right_values


def values_at_height_gpt(root: Node | None, height: int) -> list[int]:
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
    solutions: list[Callable[[Node | None, int], list[int]]] = [
        values_at_height,
        values_at_height_gpt,
    ]

    cases: list[tuple[TupleNode | None, int, list[int]]] = [
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
                    self.assertEqual(expected, solution(Node.from_tuples(root), height))


if __name__ == "__main__":
    unittest.main()
