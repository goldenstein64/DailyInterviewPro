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

from typing import Any
import unittest

from ds.binary_tree import BinaryTree, TupleBinaryTree


def invert[T](node: BinaryTree[T]) -> BinaryTree[T]:
    return BinaryTree(
        val=node.val,
        left=node.right and invert(node.right),
        right=node.left and invert(node.left),
    )


def invert_in_place(node: BinaryTree[Any]) -> None:
    node.left, node.right = node.right, node.left
    if node.left:
        invert_in_place(node.left)

    if node.right:
        invert_in_place(node.right)


class Tests(unittest.TestCase):
    @staticmethod
    def tree() -> BinaryTree[str]:
        return BinaryTree.from_tuples(((("a",), "b", ("c",)), "d", (("e",), "f")))

    cases: list[tuple[TupleBinaryTree[str], TupleBinaryTree[str]]] = [
        (
            ((("a",), "b", ("c",)), "d", (("e",), "f")),
            (("f", ("e",)), "d", (("c",), "b", ("a",))),
        )
    ]

    def test_cases(self):
        for node, expected in self.cases:
            with self.subTest(node=node, expected=expected):
                self.assertEqual(
                    BinaryTree.from_tuples(expected),
                    invert(BinaryTree.from_tuples(node)),
                )


if __name__ == "__main__":
    unittest.main()
