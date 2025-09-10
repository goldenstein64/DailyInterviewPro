"""
You are given the root of a binary search tree. Return true if it is a valid
binary search tree, and false otherwise. Recall that a binary search tree has
the property that all values in the left subtree are less than or equal to the
root, and all values in the right subtree are greater than or equal to the root.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass

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


def is_bst(root: Node | None, lo: int | None = None, hi: int | None = None) -> bool:
    if root is None:
        return True

    if lo is not None and lo > root.val:
        return False

    if hi is not None and root.val > hi:
        return False

    return is_bst(root.left, lo, root.val) and is_bst(root.right, root.val, hi)


class Tests(unittest.TestCase):
    cases: list[tuple[TupleNode | None, bool]] = [
        (None, True),
        ((1,), True),
        (((1,), 1), True),
        ((1, (1,)), True),
        (((2,), 1), False),
        (((1,), 2, (3,)), True),
        (((3,), 2, (1,)), False),
        (
            (((1,), 3, (4,)), 5, ((6,), 7)),
            True,
        ),
        (
            (((1,), 3, (4,)), 5, ((8,), 7)),
            False,
        ),
    ]

    def test_cases(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                if root is None:
                    self.assertEqual(expected, is_bst(None))
                else:
                    self.assertEqual(expected, is_bst(Node.from_tuples(root)))


if __name__ == "__main__":
    unittest.main()
