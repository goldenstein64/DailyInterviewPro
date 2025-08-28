r"""
You are given the root of a binary tree. Return the deepest node (the furthest node from the root).

Example:

>>> #     a
>>> #    / \
>>> #   b   c
>>> #  /
>>> # d
>>> tuples = ((("d",), "b"), "a", ("c",))
>>> deepest(Node.from_tuples(tuples))
Node(val='d', left=None, right=None)

Explanation: d is the farthest, at depth 3.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass

type TupleNode = (
    tuple[str]
    | tuple[TupleNode, str]
    | tuple[str, TupleNode]
    | tuple[TupleNode, str, TupleNode]
)


@dataclass
class Node:
    val: str
    left: Node | None = None
    right: Node | None = None

    @staticmethod
    def from_tuples(tuples: TupleNode) -> Node:
        match tuples:
            case (str(val),):
                return Node(val, None, None)
            case (tuple(left), str(val)):
                return Node(val, Node.from_tuples(left), None)
            case (str(val), tuple(right)):
                return Node(val, None, Node.from_tuples(right))
            case (tuple(left), str(val), tuple(right)):
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


def deepest_depth(node: Node) -> tuple[int, Node]:
    if node.left and node.right:
        left_depth, left_descendant = deepest_depth(node.left)
        right_depth, right_descendant = deepest_depth(node.right)
        if left_depth < right_depth:
            return right_depth + 1, right_descendant
        else:
            return left_depth + 1, left_descendant
    elif node.left:
        depth, descendant = deepest_depth(node.left)
        return depth + 1, descendant
    elif node.right:
        depth, descendant = deepest_depth(node.right)
        return depth + 1, descendant
    else:
        return 0, node


def deepest(node: Node) -> Node:
    return deepest_depth(node)[1]


class Tests(unittest.TestCase):
    cases: list[tuple[Node, Node]] = [
        (Node("a"), Node("a")),
        (Node("a", left=Node("b")), Node("b")),
        (Node("a", left=Node("b"), right=Node("c")), Node("b")),
        (
            Node(
                val="a",
                left=Node("b"),
                right=Node("c", left=Node("d")),
            ),
            Node("d"),
        ),
    ]

    def test_cases(self):
        for node, expected in self.cases:
            with self.subTest(node=node, expected=expected):
                self.assertEqual(expected, deepest(node))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
