"""
You are given the root of a binary tree. Return the deepest node (the furthest node from the root).

Example:
    Input:
        a
       / \
      b   c
     /
    d
    Output: d
    Because d is the farthest, at depth 3.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass


@dataclass
class Node:
    val: str
    left: Node | None = None
    right: Node | None = None


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

    def test_all(self):
        for node, expected in self.cases:
            with self.subTest(node=node, expected=expected):
                self.assertEqual(expected, deepest(node))


if __name__ == "__main__":
    unittest.main()
