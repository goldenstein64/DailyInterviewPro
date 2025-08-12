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


@dataclass
class Tree[T]:
    val: T
    left: Tree[T] | None = None
    right: Tree[T] | None = None

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


def create_bst_slice[T](values: list[T], i: int, j: int) -> Tree[T] | None:
    """Create a binary search tree from values[i:j]."""
    if i >= j:
        return None

    mid = (i + j) // 2
    return Tree(
        val=values[mid],
        left=create_bst_slice(values, i, mid),
        right=create_bst_slice(values, mid + 1, j),
    )


def create_bst[T](values: list[T]) -> Tree[T] | None:
    """Create a binary search tree from a sorted list of values."""
    return create_bst_slice(values, 0, len(values))


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], Tree[int] | None]] = [
        ([], None),
        ([1], Tree(1)),
        ([1, 2, 3], Tree(2, left=Tree(1), right=Tree(3))),
        (
            [1, 2, 3, 4, 5, 6, 7],
            Tree(
                val=4,
                left=Tree(2, left=Tree(1), right=Tree(3)),
                right=Tree(6, left=Tree(5), right=Tree(7)),
            ),
        ),
    ]

    def test_all(self):
        for values, expected in self.cases:
            with self.subTest(values=values, expected=expected):
                self.assertEqual(expected, create_bst(values))


if __name__ == "__main__":
    unittest.main()
