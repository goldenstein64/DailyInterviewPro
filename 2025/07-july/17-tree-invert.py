r"""
You are given the root of a binary tree. Invert the binary tree in place. That
is, all left children should become right children, and all right children
should become left children.

Example:

     d
   /   \
  b     f
 / \   /
a   c e

The inverted version of this tree is as follows:

   d
 /   \
f     b
 \   / \
  e c   a
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Generator

type TupleNode = (
    tuple[str]
    | tuple[TupleNode, str]
    | tuple[str, TupleNode]
    | tuple[TupleNode, str, TupleNode]
)


@dataclass
class Node:
    value: str
    left: Node | None = None
    right: Node | None = None

    def inorder(self) -> Generator[str]:
        if self.left:
            yield from self.left.inorder()

        yield self.value

        if self.right:
            yield from self.right.inorder()

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


def invert(node: Node) -> Node:
    return Node(
        value=node.value,
        left=node.right and invert(node.right),
        right=node.left and invert(node.left),
    )


def invert_in_place(node: Node) -> None:
    node.left, node.right = node.right, node.left
    if node.left:
        invert_in_place(node.left)

    if node.right:
        invert_in_place(node.right)


class Tests(unittest.TestCase):
    @staticmethod
    def tree() -> Node:
        return Node.from_tuples(((("a",), "b", ("c",)), "d", (("e",), "f")))

    cases: list[tuple[TupleNode, TupleNode]] = [
        (
            ((("a",), "b", ("c",)), "d", (("e",), "f")),
            (("f", ("e",)), "d", (("c",), "b", ("a",))),
        )
    ]

    def test_all(self):
        for node, expected in self.cases:
            with self.subTest(node=node, expected=expected):
                self.assertEqual(
                    Node.from_tuples(expected), invert(Node.from_tuples(node))
                )


if __name__ == "__main__":
    unittest.main()
