"""
Given an integer k and a binary search tree, find the floor (less than or equal
to) of k, and the ceiling (larger than or equal to) of k. If either does not
exist, then print them as None.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from itertools import product
from typing import Callable

from ds.binary_tree import BinaryTree

type TupleNode = (
    tuple[int]
    | tuple[TupleNode, int]
    | tuple[int, TupleNode]
    | tuple[TupleNode, int, TupleNode]
)

type Bounds = tuple[int | None, int | None]


@dataclass
class Node:
    value: int
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


def find_ceiling_floor_loop(root: BinaryTree[int], k: int) -> Bounds:
    floor: int | None = None
    ceil: int | None = None
    node: BinaryTree[int] | None = root
    while node is not None:
        if k < node.val:
            ceil = root.val if ceil is None else min(root.val, ceil)
            node = node.left
        elif node.val < k:
            floor = root.val if floor is None else max(root.val, floor)
            node = node.right
        else:
            return (k, k)

    return (floor, ceil)


def find_ceiling_floor(
    root: BinaryTree[int], k: int, floor: int | None = None, ceil: int | None = None
) -> Bounds:
    """
    Return (k, k) if k is in the tree. Otherwise, return the leaves closest to it.
    """
    if k < root.val:  # it's on the left
        new_ceil = root.val if ceil is None else min(root.val, ceil)
        if root.left:
            return find_ceiling_floor(root.left, k, floor, new_ceil)
        else:
            return (floor, new_ceil)
    elif root.val < k:  # it's on the right
        new_floor = root.val if floor is None else max(root.val, floor)
        if root.right:
            return find_ceiling_floor(root.right, k, new_floor, ceil)
        else:
            return (new_floor, ceil)
    else:
        return (k, k)


class Tests(unittest.TestCase):
    @staticmethod
    def tree() -> BinaryTree[int]:
        return BinaryTree.from_tuples((((2,), 4, (6,)), 8, ((10,), 12, (14,))))

    solutions: list[Callable[[BinaryTree[int], int], Bounds]] = [
        find_ceiling_floor,
        find_ceiling_floor_loop,
    ]

    cases: list[tuple[int, Bounds]] = [
        (1, (None, 2)),
        (2, (2, 2)),
        (5, (4, 6)),
        (7, (6, 8)),
        (8, (8, 8)),
        (9, (8, 10)),
        (14, (14, 14)),
        (15, (14, None)),
    ]

    def test_cases(self):
        for solution, (k, expected) in product(self.solutions, self.cases):
            tree = self.tree()
            sol = solution.__name__
            with self.subTest(solution=sol, k=k, expected=expected):
                self.assertEqual(expected, solution(tree, k))


if __name__ == "__main__":
    unittest.main()
