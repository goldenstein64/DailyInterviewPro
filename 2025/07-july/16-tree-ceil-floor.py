"""
Given an integer k and a binary search tree, find the floor (less than or equal
to) of k, and the ceiling (larger than or equal to) of k. If either does not
exist, then print them as None.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Callable
from itertools import product

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


def find_ceiling_floor_loop(root_node: Node, k: int) -> Bounds:
    floor: int | None = None
    ceil: int | None = None
    node: Node | None = root_node
    while node is not None:
        if k < node.value:
            ceil = root_node.value if ceil is None else min(root_node.value, ceil)
            node = node.left
        elif node.value < k:
            floor = root_node.value if floor is None else max(root_node.value, floor)
            node = node.right
        else:
            return (k, k)

    return (floor, ceil)


def find_ceiling_floor(
    root_node: Node, k: int, floor: int | None = None, ceil: int | None = None
) -> Bounds:
    """
    Return (k, k) if k is in the tree. Otherwise, return the leaves closest to it.
    """
    if k < root_node.value:  # it's on the left
        new_ceil = root_node.value if ceil is None else min(root_node.value, ceil)
        if root_node.left:
            return find_ceiling_floor(root_node.left, k, floor, new_ceil)
        else:
            return (floor, new_ceil)
    elif root_node.value < k:  # it's on the right
        new_floor = root_node.value if floor is None else max(root_node.value, floor)
        if root_node.right:
            return find_ceiling_floor(root_node.right, k, new_floor, ceil)
        else:
            return (new_floor, ceil)
    else:
        return (k, k)


class Tests(unittest.TestCase):
    @staticmethod
    def tree() -> Node:
        return Node.from_tuples((((2,), 4, (6,)), 8, ((10,), 12, (14,))))

    solutions: list[Callable[[Node, int], Bounds]] = [
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

    def test_all(self):
        for solution, (k, expected) in product(self.solutions, self.cases):
            tree = self.tree()
            sol = solution.__name__
            with self.subTest(solution=sol, k=k, expected=expected):
                self.assertEqual(expected, solution(tree, k))


if __name__ == "__main__":
    unittest.main()
