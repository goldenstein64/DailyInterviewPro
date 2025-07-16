"""
Given an integer k and a binary search tree, find the floor (less than or equal
to) of k, and the ceiling (larger than or equal to) of k. If either does not
exist, then print them as None.
"""

from __future__ import annotations

from dataclasses import dataclass
import unittest


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None


def find_ceiling_floor(
    root_node: Node, k: int, floor: int | None = None, ceil: int | None = None
) -> tuple[int | None, int | None]:
    """
    How would I approach this?

    This is really the same thing as saying "is k in the tree? If so, return
    (k, k). If not, give me the two numbers it's between.
    """
    if k < root_node.value:  # it's on the left
        new_ceil = min(root_node.value, ceil) if ceil else root_node.value
        if root_node.left:
            return find_ceiling_floor(root_node.left, k, floor, new_ceil)
        else:
            return (floor, new_ceil)
    elif root_node.value < k:  # it's on the right
        new_floor = max(root_node.value, floor) if floor else root_node.value
        if root_node.right:
            return find_ceiling_floor(root_node.right, k, new_floor, ceil)
        else:
            return (new_floor, ceil)
    else:
        return (k, k)


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
        for k, expected in self.cases:
            self.assertEqual(expected, find_ceiling_floor(tree, k))


if __name__ == "__main__":
    unittest.main()
