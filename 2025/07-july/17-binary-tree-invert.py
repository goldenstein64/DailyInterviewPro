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
        return Node(
            value="d",
            left=Node(
                value="b",
                left=Node(value="a"),
                right=Node(value="c"),
            ),
            right=Node(
                value="f",
                left=Node(value="e"),
            ),
        )

    def test_tree(self):
        tree = self.tree()
        self.assertEqual("abcdef", "".join(tree.inorder()))
        self.assertEqual("fedcba", "".join(invert(tree).inorder()))
        invert_in_place(tree)
        self.assertEqual("fedcba", "".join(tree.inorder()))


if __name__ == "__main__":
    unittest.main()
