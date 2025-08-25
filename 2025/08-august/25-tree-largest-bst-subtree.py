"""
You are given the root of a binary tree. Find and return the largest subtree of
that tree, which is a valid binary search tree.

Examples:

>>> largest_bst_subtree(Node(1)).as_tuples()
(1,)

>>> node = Node.from_tuples(((1,), 1))
>>> largest_bst_subtree(node).as_tuples()
(1,)

>>> node = Node.from_tuples(((1,), 2, (3,)))
>>> largest_bst_subtree(node).as_tuples()
((1,), 2, (3,))

>>> node = Node.from_tuples(
...     (((2,), 6), 5, ((4,), 7, (9,)))
... )
>>> largest_bst_subtree(node).as_tuples()
((4,), 7, (9,))

>>> node = Node.from_tuples(
...     (((2,), 4), 5, ((6,), 7, (9,)))
... )
>>> largest_bst_subtree(node).as_tuples()
(((2,), 4), 5, ((6,), 7, (9,)))
"""

from __future__ import annotations
from dataclasses import dataclass
import unittest

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


@dataclass
class BSTSubtreeResult:
    """an internal data structure for the largest_bst_subtree algorithm"""

    node: Node
    size: int
    min: int
    max: int


def largest_bst_subtree_inner(root: Node) -> BSTSubtreeResult:
    match (root.left, root.right):
        case (Node() as left, Node() as right):
            subtree_left = largest_bst_subtree_inner(left)
            subtree_right = largest_bst_subtree_inner(right)
            # try to expand the tree
            if (
                subtree_left.node == left
                and subtree_right.node == right
                and root.val > subtree_left.max
                and root.val < subtree_right.min
            ):
                return BSTSubtreeResult(
                    node=root,
                    size=subtree_left.size + subtree_right.size + 1,
                    min=subtree_left.min,
                    max=subtree_right.max,
                )

            return max(subtree_left, subtree_right, key=lambda st: st.size)
        case (Node() as left, None):
            subtree = largest_bst_subtree_inner(left)
            # try to expand the tree
            if subtree.node == left and root.val > subtree.max:
                return BSTSubtreeResult(
                    node=root,
                    size=subtree.size + 1,
                    min=subtree.min,
                    max=root.val,
                )

            return subtree
        case (None, Node() as right):
            subtree = largest_bst_subtree_inner(right)
            # try to expand the tree
            if subtree.node == right and root.val < subtree.min:
                return BSTSubtreeResult(
                    node=root,
                    size=subtree.size + 1,
                    min=root.val,
                    max=subtree.max,
                )

            return subtree
        case (None, None):
            return BSTSubtreeResult(node=root, size=1, min=root.val, max=root.val)


class Tests(unittest.TestCase):
    cases: list[tuple[TupleNode, TupleNode]] = [
        ((1,), (1,)),
        (((1,), 1), (1,)),
        ((1, (1,)), (1,)),
        ((1, (0,)), (0,)),
        ((((10,), 5), 2, (1,)), (10,)),
        (((1,), 2, (3,)), ((1,), 2, (3,))),
        (((2,), 1, (3,)), (2,)),
        ((((2,), 6), 5, ((4,), 7, (9,))), ((4,), 7, (9,))),
        ((((2,), 4), 5, ((6,), 7, (9,))), (((2,), 4), 5, ((6,), 7, (9,)))),
    ]

    def test_all(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                self.assertEqual(
                    Node.from_tuples(expected),
                    largest_bst_subtree(Node.from_tuples(root)),
                )


def largest_bst_subtree(root: Node) -> Node:
    """
    Return the largest binary search tree subtree of `root`.

    Generally, we can start at a leaf node, move up to its parent, and if the
    parent and other branch is on the correct side of the search tree, then the
    entire thing can be a binary search tree
    """
    return largest_bst_subtree_inner(root).node


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
