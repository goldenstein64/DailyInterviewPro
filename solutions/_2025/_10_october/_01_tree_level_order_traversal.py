"""
Given the root of a binary tree, print its level-order traversal.

Example:

>>> root = BinaryTree.from_tuples(((2,), 1, ((4,), 3, (5,))))
>>> [node.val for node in level_order_traversal(root)]
[1, 2, 3, 4, 5]
"""

import unittest
from collections import deque
from collections.abc import Generator

from ds.binary_tree import BinaryTree, TupleBinaryTree


def level_order_traversal[T](root: BinaryTree[T]) -> Generator[BinaryTree[T]]:
    nodes: deque[BinaryTree[T]] = deque()
    nodes.append(root)
    while nodes:
        node: BinaryTree[T] = nodes.popleft()
        yield node
        if left := node.left:
            nodes.append(left)

        if right := node.right:
            nodes.append(right)


class Tests(unittest.TestCase):
    cases: list[tuple[TupleBinaryTree[int], list[int]]] = [
        ((1,), [1]),
        (((2,), 1, (3,)), [1, 2, 3]),
        ((((3,), 2), 1), [1, 2, 3]),
        ((1, (2, (3,))), [1, 2, 3]),
        (((2,), 1, ((4,), 3, (5,))), [1, 2, 3, 4, 5]),
        ((((4,), 2, (5,)), 1, ((6,), 3, (7,))), [1, 2, 3, 4, 5, 6, 7]),
    ]

    def test_cases(self):
        for tuples, expected in self.cases:
            with self.subTest(root=tuples, expected=expected):
                root: BinaryTree[int] = BinaryTree.from_tuples(tuples)
                traversal: list[int] = [
                    node.val for node in level_order_traversal(root)
                ]
                self.assertEqual(expected, traversal)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
