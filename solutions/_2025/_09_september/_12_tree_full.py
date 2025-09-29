"""
Given a binary tree, remove the nodes in which there is only 1 child, so that
the binary tree is a full binary tree.

So leaf nodes with no children should be kept, and nodes with 2 children should
be kept as well.

Example:

>>> tree = BinaryTree.from_tuples((((0,), 2), 1, ((9,), 3, (4,))))
>>> full_binary_tree(tree).as_tuples()
((0,), 1, ((9,), 3, (4,)))
"""

from ds.binary_tree import BinaryTree, TupleBinaryTree
from typing import overload
import unittest


@overload
def full_binary_tree(root: None) -> None: ...
@overload
def full_binary_tree(root: BinaryTree[int]) -> BinaryTree[int]: ...
def full_binary_tree(root: BinaryTree[int] | None) -> BinaryTree[int] | None:
    match root:
        case None:
            return None
        case BinaryTree(val, BinaryTree() as left, BinaryTree() as right):
            return BinaryTree(val, full_binary_tree(left), full_binary_tree(right))
        case BinaryTree(val, BinaryTree() as child, None) | BinaryTree(
            val, None, BinaryTree() as child
        ):
            return full_binary_tree(child)
        case BinaryTree(val, None, None):
            return BinaryTree(val)
        case BinaryTree():
            raise ValueError
        case _:
            raise TypeError


class Tests(unittest.TestCase):
    cases: list[tuple[TupleBinaryTree[int], TupleBinaryTree[int]]] = [
        ((1,), (1,)),
        (((1,), 2), (1,)),
        ((1, (2,)), (2,)),
        (((1,), 2, (3,)), ((1,), 2, (3,))),
        ((((0,), 2), 1, ((9,), 3, (4,))), ((0,), 1, ((9,), 3, (4,)))),
    ]

    def test_cases(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                self.assertEqual(
                    BinaryTree.from_tuples(expected),
                    full_binary_tree(BinaryTree.from_tuples(root)),
                )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
