r"""
Given a sorted list of numbers, change it into a balanced binary search tree.
You can assume there will be no duplicate numbers in the list.

Example:
    Input: [1, 2, 3, 4, 5, 6, 7]
    Output:
           4
          / \
         2   6
        / \ / \
        1 3 5 7
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


def create_bst_slice(values: list[int], i: int, j: int) -> Node | None:
    """Create a binary search tree from values[i:j]."""
    if i >= j:
        return None

    mid = (i + j) // 2
    return Node(
        val=values[mid],
        left=create_bst_slice(values, i, mid),
        right=create_bst_slice(values, mid + 1, j),
    )


def create_bst(values: list[int]) -> Node | None:
    """Create a binary search tree from a sorted list of values."""
    return create_bst_slice(values, 0, len(values))


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], TupleNode | None]] = [
        ([], None),
        ([1], (1,)),
        ([1, 2, 3], ((1,), 2, (3,))),
        (
            [1, 2, 3, 4, 5, 6, 7],
            (((1,), 2, (3,)), 4, ((5,), 6, (7,))),
        ),
    ]

    def test_all(self):
        for values, expected in self.cases:
            with self.subTest(values=values, expected=expected):
                if expected is None:
                    self.assertIsNone(create_bst(values))
                else:
                    self.assertEqual(Node.from_tuples(expected), create_bst(values))


if __name__ == "__main__":
    unittest.main()
