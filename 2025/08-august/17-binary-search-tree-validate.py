"""
You are given the root of a binary search tree. Return true if it is a valid
binary search tree, and false otherwise. Recall that a binary search tree has
the property that all values in the left subtree are less than or equal to the
root, and all values in the right subtree are greater than or equal to the root.
"""

from __future__ import annotations


import unittest
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Tree:
    val: int
    left: Tree | None = None
    right: Tree | None = None

    def str_buffer(self, buffer: list[str], depth: int) -> None:
        indent = "  " * depth
        if self.right:
            self.right.str_buffer(buffer, depth + 1)
            buffer.append(f"{indent} /")

        buffer.append(f"{indent}{self.val}")

        if self.left:
            buffer.append(f"{indent} \\")
            self.left.str_buffer(buffer, depth + 1)

    def __str__(self) -> str:
        buffer: list[str] = []
        self.str_buffer(buffer, 0)
        return "\n".join(buffer)


def is_bst(root: Tree | None, lo: int | None = None, hi: int | None = None) -> bool:
    if root is None:
        return True

    if lo is not None and lo > root.val:
        return False

    if hi is not None and root.val > hi:
        return False

    return is_bst(root.left, lo, root.val) and is_bst(root.right, root.val, hi)


class Tests(unittest.TestCase):
    cases: ClassVar[list[tuple[Tree | None, bool]]] = [
        (None, True),
        (Tree(1), True),
        (Tree(1, left=Tree(1)), True),
        (Tree(1, right=Tree(1)), True),
        (Tree(1, left=Tree(2)), False),
        (Tree(2, left=Tree(1), right=Tree(3)), True),
        (Tree(2, left=Tree(3), right=Tree(1)), False),
        (
            Tree(
                val=5,
                left=Tree(3, left=Tree(1), right=Tree(4)),
                right=Tree(7, left=Tree(6)),
            ),
            True,
        ),
        (
            Tree(
                val=5,
                left=Tree(3, left=Tree(1), right=Tree(4)),
                right=Tree(7, left=Tree(8)),
            ),
            False,
        ),
    ]

    def test_all(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                self.assertEqual(expected, is_bst(root))


if __name__ == "__main__":
    unittest.main()
