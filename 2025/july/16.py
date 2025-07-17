"""
Given an integer k and a binary search tree, find the floor (less than or equal
to) of k, and the ceiling (larger than or equal to) of k. If either does not
exist, then print them as None.
"""

from __future__ import annotations

from dataclasses import dataclass
import unittest
from typing import Callable


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def find_ceiling_floor_loop(root_node: Node, k: int) -> tuple[int | None, int | None]:
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
) -> tuple[int | None, int | None]:
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


type Solution = Callable[[Node, int], tuple[int | None, int | None]]


class Tests(unittest.TestCase):
    @staticmethod
    def tree() -> Node:
        return Node(
            value=8,
            left=Node(
                value=4,
                left=Node(value=2),
                right=Node(value=6),
            ),
            right=Node(
                value=12,
                left=Node(value=10),
                right=Node(value=14),
            ),
        )

    cases: list[tuple[int, tuple[int | None, int | None]]] = [
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
        tree = self.tree()
        solutions: list[Solution] = [find_ceiling_floor, find_ceiling_floor_loop]
        for solution in solutions:
            for k, expected in self.cases:
                with self.subTest(solution=solution.__name__, k=k, expected=expected):
                    self.assertEqual(expected, solution(tree, k))


if __name__ == "__main__":
    unittest.main()
